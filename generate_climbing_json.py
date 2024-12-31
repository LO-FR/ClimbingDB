import csv
import json
import os
from flask import Flask, request, jsonify, render_template

# File paths
REGIONS_FILE = "regions_and_provinces.csv"
JSON_FILE = "climbing_spots.json"

# Global dictionaries for region and province lookup
REGION_CODES = {}
PROVINCE_CODES = {}

def load_regions_and_provinces(regions_file):
    """Load regions and provinces from a CSV file into dictionaries."""
    global REGION_CODES, PROVINCE_CODES
    with open(regions_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            REGION_CODES[row["region_name"]] = row["region_id"]
            PROVINCE_CODES[row["province_name"]] = row["province_id"]

def load_json():
    """Load the existing JSON file or create a new one if it doesn't exist."""
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w") as file:
            json.dump({"countries": []}, file, ensure_ascii=False, indent=4)
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_json(data):
    """Save the updated data back to the JSON file."""
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Flask setup
APP = Flask(__name__)

@APP.route("/")
def index():
    return render_template("index.html")

@APP.route("/add", methods=["POST"])
def add_data():
    # Load data
    data = load_json()

    # Read data from the form
    country_id = "ITA"  # Static for Italy
    country_name = "Italy"
    region_name = request.form["region_name"]
    province_name = request.form["province_name"]
    cliff_name = request.form["cliff_name"]
    cliff_latitude = float(request.form["cliff_latitude"])
    cliff_longitude = float(request.form["cliff_longitude"])

    # Get IDs from dictionaries
    region_id = REGION_CODES.get(region_name)
    province_id = PROVINCE_CODES.get(province_name)

    # Validate IDs
    if not region_id or not province_id:
        return jsonify({"error": "Region or province not found in the database."}), 400

    # Add or update the JSON structure
    country = next((c for c in data["countries"] if c["id"] == country_id), None)
    if not country:
        country = {"id": country_id, "name": country_name, "regions": []}
        data["countries"].append(country)

    region = next((r for r in country["regions"] if r["id"] == region_id), None)
    if not region:
        region = {"id": region_id, "name": region_name, "provinces": []}
        country["regions"].append(region)

    province = next((p for p in region["provinces"] if p["id"] == province_id), None)
    if not province:
        province = {"id": province_id, "name": province_name, "cliffs": []}
        region["provinces"].append(province)

    # Add a new cliff
    cliff_id = f"{province_id}{len(province['cliffs']) + 1:05}"
    cliff = {
        "id": cliff_id,
        "name": cliff_name,
        "maps": {
            "latitude": cliff_latitude,
            "longitude": cliff_longitude,
            "link": f"https://maps.google.com/?q={cliff_latitude},{cliff_longitude}"
        },
        "sectors": []
    }
    province["cliffs"].append(cliff)

    # Save the updated JSON
    save_json(data)

    return jsonify({"message": "Cliff added successfully", "cliff_id": cliff_id})

if __name__ == "__main__":
    # Load region and province data
    load_regions_and_provinces(REGIONS_FILE)
    # Run the Flask app
    APP.run(debug=True)
