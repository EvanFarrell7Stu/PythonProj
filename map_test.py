import geopandas as gpd
import pandas as pd
import folium
from branca.colormap import linear

def load_constituencies(geojson_path):
    # load your constituencies boundaries (GeoJSON or Shapefile)
    gdf = gpd.read_file(geojson_path)
    # ensure a common CRS (latitude/longitude, WGS84)
    gdf = gdf.to_crs(epsg=4326)
    return gdf

def load_results(results_csv_path):
    # load a CSV (or other) with columns like: constituency_id / name, winner_party, vote_share etc.
    df = pd.read_csv(results_csv_path)
    return df

def make_election_map(geojson_path, results_csv_path, output_html="election_map.html"):
    gdf = load_constituencies(geojson_path)
    df = load_results(results_csv_path)

    # Merge geometry + results
    merged = gdf.merge(df, on="constituency_id", how="left")

    # Choose a colormap for, say, vote share or winner
    # Example: color by vote_share (0 to 100) — adjust as needed
    minv = merged["vote_share"].min()
    maxv = merged["vote_share"].max()
    colormap = linear.YlOrRd_09.scale(minv, maxv)
    colormap.caption = "Vote Share (%)"

    # Create base folium map
    # Center roughly over Ireland
    m = folium.Map(location=[53.3, -8.0], zoom_start=7, tiles="CartoDB.Positron")

    # Function to style each polygon
    def style_function(feature):
        # If a constituency has no data, color it gray
        vs = feature["properties"].get("vote_share")
        if vs is None:
            return {
                "fillColor": "#cccccc",
                "color": "black",
                "weight": 0.5,
                "fillOpacity": 0.6,
            }
        return {
            "fillColor": colormap(vs),
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.8,
        }

    # Add GeoJson layer
    folium.GeoJson(
        merged,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=["constituency_name", "winner_party", "vote_share"],
            aliases=["Constituency:", "Winner:", "Vote share (%) :"],
            localize=True
        )
    ).add_to(m)

    # Add the color scale (legend)
    colormap.add_to(m)

    # Save to HTML
    m.save(output_html)
    print("Map saved to", output_html)


if __name__ == "__main__":
    # Example usage (you replace with your actual file paths)
    geojson_path = "path/to/constituencies.geojson"
    results_csv_path = "path/to/results.csv"
    make_election_map(geojson_path, results_csv_path)
