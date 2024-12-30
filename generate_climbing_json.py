import csv
import json

# File paths
REGIONS_FILE = "regions_and_provinces.csv"
CSV_FILE = "climbing_spots.csv"
OUTPUT_FILE = "climbing_spots.json"

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

def generate_cliff_id(province_id, cliff_count):
    """Generate a unique ID for a cliff with 5-digit zero-fill."""
    return f"{province_id}{str(cliff_count).zfill(5)}"

def generate_sector_id(cliff_id, sector_count):
    """Generate a unique ID for a sector."""
    return f"{cliff_id}{chr(65 + sector_count)}"  # Append A, B, C...

def generate_route_id(sector_id, route_count):
    """Generate a unique ID for a route with 4-digit zero-fill."""
    return f"{sector_id}{str(route_count).zfill(4)}"

def generate_json_from_csv(csv_file):
    data = {"countries": []}
    country_dict = {}

    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            country_id = row["country_id"]
            if country_id not in country_dict:
                # Create new country
                country = {
                    "id": country_id,
                    "name": row["country_name"],
                    "regions": []
                }
                country_dict[country_id] = country
                data["countries"].append(country)

            country = country_dict[country_id]

            region_name = row["region_name"]
            region_id = REGION_CODES.get(region_name)
            if region_id and all(r["id"] != region_id for r in country["regions"]):
                # Create new region
                region = {
                    "id": region_id,
                    "name": region_name,
                    "provinces": []
                }
                country["regions"].append(region)

            region = next(r for r in country["regions"] if r["id"] == region_id)

            province_name = row["province_name"]
            province_id = PROVINCE_CODES.get(province_name)
            if province_id and all(p["id"] != province_id for p in region["provinces"]):
                # Create new province
                province = {
                    "id": province_id,
                    "name": province_name,
                    "cliffs": []
                }
                region["provinces"].append(province)

            province = next(p for p in region["provinces"] if p["id"] == province_id)

            # Count cliffs dynamically
            cliff_count = len(province["cliffs"]) + 1
            cliff_id = generate_cliff_id(province_id, cliff_count)
            cliff_name = row["cliff_name"]
            if cliff_name and all(c["id"] != cliff_id for c in province["cliffs"]):
                # Create new cliff
                cliff = {
                    "id": cliff_id,
                    "name": cliff_name,
                    "maps": {
                        "latitude": float(row["cliff_latitude"]),
                        "longitude": float(row["cliff_longitude"]),
                        "link": f"https://maps.google.com/?q={row['cliff_latitude']},{row['cliff_longitude']}"
                    },
                    "sectors": []
                }
                province["cliffs"].append(cliff)

            cliff = next(c for c in province["cliffs"] if c["id"] == cliff_id)

            # Count sectors dynamically
            sector_count = len(cliff["sectors"])
            sector_id = generate_sector_id(cliff_id, sector_count)
            sector_name = row["sector_name"]
            if sector_name and all(s["id"] != sector_id for s in cliff["sectors"]):
                # Create new sector
                sector = {
                    "id": sector_id,
                    "name": sector_name,
                    "maps": {
                        "latitude": float(row["sector_latitude"]) if row["sector_latitude"] else 0,
                        "longitude": float(row["sector_longitude"]) if row["sector_longitude"] else 0,
                        "link": f"https://maps.google.com/?q={row['sector_latitude']},{row['sector_longitude']}"
                    },
                    "routes": []
                }
                cliff["sectors"].append(sector)

            sector = next(s for s in cliff["sectors"] if s["id"] == sector_id)

            # Count routes dynamically
            route_count = len(sector["routes"]) + 1
            route_id = generate_route_id(sector_id, route_count)
            route_name = row["route_name"]
            if route_name and all(r["id"] != route_id for r in sector["routes"]):
                # Create new route
                route = {
                    "id": route_id,
                    "name": route_name,
                    "grade": row["route_grade"],
                    "photos": []
                }
                sector["routes"].append(route)

    return data

def main():
    # Load regions and provinces
    load_regions_and_provinces(REGIONS_FILE)

    # Generate JSON from climbing spots CSV
    data = generate_json_from_csv(CSV_FILE)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"JSON saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
