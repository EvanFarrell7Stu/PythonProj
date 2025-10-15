# PythonProj

A Python application that reads location data from a CSV file and displays the data points on an interactive map of Ireland.

## Features

- Reads location data from CSV files
- Creates an interactive map centered on Ireland
- Displays markers with location names and descriptions
- Generates an HTML map file that can be opened in any web browser

## Requirements

- Python 3.7 or higher
- pandas
- folium

## Installation

1. Clone this repository:
```bash
git clone https://github.com/EvanFarrell7Stu/PythonProj.git
cd PythonProj
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Using the default CSV file

The application comes with a sample `locations.csv` file containing popular Irish locations:

```bash
python map_app.py
```

### Using a custom CSV file

You can provide your own CSV file as a command-line argument:

```bash
python map_app.py path/to/your/locations.csv
```

### CSV File Format

Your CSV file should contain the following columns:
- `name`: Name of the location
- `latitude`: Latitude coordinate
- `longitude`: Longitude coordinate
- `description`: Description of the location

Example CSV format:
```csv
name,latitude,longitude,description
Dublin,53.3498,-6.2603,Capital city of Ireland
Cork,51.8969,-8.4863,Second largest city
```

## Output

The application generates an `ireland_map.html` file in the current directory. Open this file in your web browser to view the interactive map with all the locations from your CSV file.

## Sample Data

The included `locations.csv` file contains the following Irish locations:
- Dublin (Capital city)
- Cork (Second largest city)
- Galway (West coast city)
- Limerick (Mid-West city)
- Waterford (South-East city)
- Killarney (Town in County Kerry)
- Cliffs of Moher (Famous coastal cliffs)
- Ring of Kerry (Scenic tourist route)
- Giant's Causeway (UNESCO World Heritage Site)
- Blarney Castle (Historic castle near Cork)

## License

This project is open source and available under the MIT License.