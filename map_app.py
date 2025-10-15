#!/usr/bin/env python3
"""
Python application that reads a CSV file and displays data points on a map of Ireland.
"""

import pandas as pd
import folium
import os
import sys


def read_csv_data(csv_file):
    """
    Read location data from a CSV file.
    
    Args:
        csv_file (str): Path to the CSV file
        
    Returns:
        pandas.DataFrame: DataFrame containing the location data
    """
    try:
        df = pd.read_csv(csv_file)
        print(f"Successfully read {len(df)} locations from {csv_file}")
        return df
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)


def create_ireland_map(data, output_file='ireland_map.html'):
    """
    Create an interactive map of Ireland with data points from the CSV.
    
    Args:
        data (pandas.DataFrame): DataFrame containing location data with columns:
                                 name, latitude, longitude, description
        output_file (str): Name of the output HTML file
    """
    # Center the map on Ireland (approximate center coordinates)
    ireland_center = [53.1424, -7.6921]
    
    # Create a map centered on Ireland
    map_ireland = folium.Map(
        location=ireland_center,
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Add markers for each location in the CSV
    for idx, row in data.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(
                f"<b>{row['name']}</b><br>{row['description']}",
                max_width=300
            ),
            tooltip=row['name'],
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(map_ireland)
    
    # Save the map to an HTML file
    map_ireland.save(output_file)
    print(f"Map saved to {output_file}")
    print(f"Open {output_file} in your web browser to view the map.")


def main():
    """
    Main function to run the application.
    """
    # Default CSV file
    csv_file = 'locations.csv'
    
    # Allow user to specify a different CSV file as command-line argument
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    
    print("=" * 50)
    print("Ireland Map Visualization Application")
    print("=" * 50)
    
    # Read the CSV data
    data = read_csv_data(csv_file)
    
    # Validate required columns
    required_columns = ['name', 'latitude', 'longitude', 'description']
    missing_columns = [col for col in required_columns if col not in data.columns]
    
    if missing_columns:
        print(f"Error: CSV file is missing required columns: {missing_columns}")
        print(f"Required columns: {required_columns}")
        sys.exit(1)
    
    print("\nLocations to be mapped:")
    for idx, row in data.iterrows():
        print(f"  - {row['name']} ({row['latitude']}, {row['longitude']})")
    
    # Create the map
    print("\nCreating map...")
    create_ireland_map(data)
    
    print("\n" + "=" * 50)
    print("Map creation complete!")
    print("=" * 50)


if __name__ == '__main__':
    main()
