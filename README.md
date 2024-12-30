# Climbing Spots JSON Structure

This repository contains structured JSON data representing climbing spots, including details about countries, regions, provinces, cliffs, sectors, and routes.

## JSON Hierarchy

The data is organized as follows:
Country > Region > Province > Cliff > Sector > Route


### Fields Description

#### **Country**
- `id` (string): Unique identifier for the country (ISO code).
- `name` (string): Name of the country.

#### **Region**
- `id` (string): Unique identifier for the region (`country_id` + region code).
- `name` (string): Name of the region.

#### **Province**
- `id` (string): Unique identifier for the province (`region_id` + province code).
- `name` (string): Name of the province.

#### **Cliff**
- `id` (string): Unique identifier for the cliff (`province_id` + cliff code).
- `name` (string): Name of the cliff.
- `exposure` (string): Orientation (e.g., North, South).
- `recommended_season` (string): Best climbing season.
- `description` (string): Description of the cliff.
- `maps` (object): Geographic data.
  - `latitude` (float): Latitude coordinate.
  - `longitude` (float): Longitude coordinate.
  - `link` (string): Link to Google Maps.

#### **Sector**
- `id` (string): Unique identifier for the sector (`cliff_id` + sector code).
- `name` (string): Name of the sector.
- `exposure` (string): Orientation (e.g., East, West).
- `recommended_season` (string): Best climbing season.
- `description` (string): Description of the sector.
- `maps` (object): Geographic data.
  - `latitude` (float): Latitude coordinate.
  - `longitude` (float): Longitude coordinate.
  - `link` (string): Link to Google Maps.

#### **Route**
- `name` (string): Name of the route.
- `grade` (string): Difficulty grade (e.g., 6a, 7b).
- `description` (string): Description of the route.
- `photos` (array): URLs to photos of the route.

### How to Use
1. Clone this repository.
2. Use the provided Python script (`generate_climbing_json.py`) to create or modify the JSON.
3. Integrate the JSON into your app or API.

### Contributing
- Feel free to add or edit data.
- Ensure the structure matches the hierarchy described above.
- Add meaningful descriptions and accurate coordinates.

### License
This project is open-source and available under the [MIT License](LICENSE).
