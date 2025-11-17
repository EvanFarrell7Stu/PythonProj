import json
import tkinter as tk

WINDOW_W = 900
WINDOW_H = 1100


class CountyMapApp:
    def __init__(self, master):
        self.master = master
        master.title("Ireland County Map")

        self.canvas = tk.Canvas(master, width=WINDOW_W, height=WINDOW_H, bg="lightblue")
        self.canvas.pack()

        # Load county shapes
        with open("ireland_counties.geojson", "r", encoding="utf-8") as f:
            self.geo = json.load(f)

        # FIELD NAME FIXED FOR YOUR FILE
        self.name_field = "NAME_1"

        # Example data (you can add more)
        self.county_data = {
            "Carlow": "Population: 61,931",
            "Donegal": "Population: 166,321",
            "Cork": "Population: 542,868",
            "Dublin": "Population: 1,450,701",
        }

        # Tooltip
        self.tooltip = tk.Label(
            self.canvas, text="", bg="white", fg="black",
            borderwidth=1, relief="solid", font=("Arial", 10)
        )
        self.tooltip.place_forget()

        self.county_items = {}
        self.draw_map()

        self.canvas.bind("<Motion>", self.on_mouse_move)

    def project(self, lon, lat):
        """Convert lat/lon into pixel coordinates."""
        min_lon, max_lon = -10.7, -5.3
        min_lat, max_lat = 51.3, 55.5

        x = (lon - min_lon) / (max_lon - min_lon) * WINDOW_W
        y = WINDOW_H - (lat - min_lat) / (max_lat - min_lat) * WINDOW_H
        return x, y

    def draw_map(self):
        """Draw each county polygon."""
        for feature in self.geo["features"]:

            county_name = feature["properties"][self.name_field]

            geom = feature["geometry"]

            # Handle Polygon vs MultiPolygon
            if geom["type"] == "Polygon":
                polygons = [geom["coordinates"]]
            else:  # MultiPolygon
                polygons = [poly for poly in geom["coordinates"]]

            for poly in polygons:
                coords = []
                for lon, lat in poly[0]:
                    x, y = self.project(lon, lat)
                    coords.append((x, y))

                item_id = self.canvas.create_polygon(
                    coords, fill="#b0c4de", outline="white", width=1
                )

                self.county_items[item_id] = county_name

    def on_mouse_move(self, event):
        """Highlight county and show tooltip."""
        items = self.canvas.find_closest(event.x, event.y)
        if not items:
            self.tooltip.place_forget()
            return

        item = items[0]

        if item not in self.county_items:
            self.tooltip.place_forget()
            return

        county = self.county_items[item]

        # Reset all colors
        for poly in self.county_items:
            self.canvas.itemconfig(poly, fill="#b0c4de")

        # Highlight hovered county
        self.canvas.itemconfig(item, fill="#809fc4")

        # Tooltip text
        info = self.county_data.get(county, "No data available")
        self.tooltip.config(text=f"{county}\n{info}")

        # Move tooltip
        self.tooltip.place(x=event.x + 15, y=event.y + 10)


root = tk.Tk()
app = CountyMapApp(root)
root.mainloop()
