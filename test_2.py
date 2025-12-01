import json
import tkinter as tk
import pandas as pd

WINDOW_W = 900
WINDOW_H = 1100

class CountyMapApp:
    def __init__(self, master):
        self.master = master
        master.title("Ireland County Map")

        self.canvas = tk.Canvas(master, width=WINDOW_W, height=WINDOW_H, bg="lightblue")
        self.canvas.pack()

        # Load GeoJSON
        with open("ireland_counties.geojson", "r", encoding="utf-8") as f:
            self.geo = json.load(f)

        # FIELD NAME in your file
        self.name_field = "NAME_1"

        # ---------------------------------------
        # LOAD EXCEL ENERGY TABLE
        # ---------------------------------------
        df = pd.read_excel("county_energy_averages.xlsx")

        # Normalize names: "Co. Carlow" → "Carlow"
        df["CleanName"] = df["CountyName"].str.replace("Co. ", "", regex=False)

        # Convert to dictionary
        self.energy_data = dict(zip(df["CleanName"], df["EnergyRatingValue"]))

        # Tooltip widget
        self.tooltip = tk.Label(
            self.canvas, text="", bg="white", fg="black",
            borderwidth=1, relief="solid", font=("Arial", 10)
        )
        self.tooltip.place_forget()

        self.county_items = {}
        self.draw_map()

        self.canvas.bind("<Motion>", self.on_mouse_move)

    def project(self, lon, lat):
        min_lon, max_lon = -10.7, -5.3
        min_lat, max_lat = 51.3, 55.5

        x = (lon - min_lon) / (max_lon - min_lon) * WINDOW_W
        y = WINDOW_H - (lat - min_lat) / (max_lat - min_lat) * WINDOW_H
        return x, y

    def get_color(self, value):
        """Colour scale based on energy rating (1–5)."""
        colors = {
            1: "#ffcccc",
            2: "#ff9999",
            3: "#ff6666",
            4: "#cc3333",
            5: "#990000",
        }
        return colors.get(value, "#b0c4de")

    def draw_map(self):
        for feature in self.geo["features"]:
            county_name = feature["properties"][self.name_field]

            # Look up energy rating
            energy_value = self.energy_data.get(county_name)

            fill_color = self.get_color(energy_value)

            geom = feature["geometry"]

            if geom["type"] == "Polygon":
                polygons = [geom["coordinates"]]
            else:
                polygons = [poly for poly in geom["coordinates"]]

            for poly in polygons:
                coords = []
                for lon, lat in poly[0]:
                    x, y = self.project(lon, lat)
                    coords.append((x, y))

                item_id = self.canvas.create_polygon(
                    coords, fill=fill_color, outline="white", width=1
                )
                self.county_items[item_id] = county_name

    def on_mouse_move(self, event):
        items = self.canvas.find_closest(event.x, event.y)
        if not items:
            self.tooltip.place_forget()
            return

        item = items[0]
        if item not in self.county_items:
            self.tooltip.place_forget()
            return

        county = self.county_items[item]

        # Reset colours
        for poly in self.county_items:
            original_value = self.energy_data.get(self.county_items[poly])
            self.canvas.itemconfig(poly, fill=self.get_color(original_value))

        # Highlight county
        original_value = self.energy_data.get(county)
        highlight_color = "#80bfff"
        self.canvas.itemconfig(item, fill=highlight_color)

        # Tooltip text
        energy = self.energy_data.get(county, "No data")
        self.tooltip.config(text=f"{county}\nEnergy Rating: {energy}")

        self.tooltip.place(x=event.x + 15, y=event.y + 10)


root = tk.Tk()
app = CountyMapApp(root)
root.mainloop()
