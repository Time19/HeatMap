import glob
import gpxpy
import folium
import os
from folium.plugins import HeatMap


project_directory = os.path.abspath(os.path.dirname(__file__))
resources_directory = os.path.join(project_directory, "resources")


# Initialisiere die Liste, um die Koordinaten zu speichern
coordinates = []


# Alle gpx Dateien durchlaufen, Koordinaten speichern
for gpx_file in glob.glob(project_directory + "\\resources\\gps_files\\*.gpx"):
    with open(gpx_file, 'r') as f:
        gpx = gpxpy.parse(f)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    coordinates.append((point.latitude, point.longitude))

# Koordinaten in einer Datei speichern
with open(project_directory + '\\resources\\coordinates.txt', 'w') as f:
    for coord in coordinates:
        f.write(f"{coord[0]},{coord[1]}\n")

# Karte erstellen
map = folium.Map(location=[sum(lat for lat, lon in coordinates) / len(coordinates),
                           sum(lon for lat, lon in coordinates) / len(coordinates)],
                 zoom_start=12)

heatmap_data = [[lat, lon] for lat, lon in coordinates]
folium.plugins.HeatMap(heatmap_data, radius=15, max_zoom=10).add_to(map)

map.save(project_directory + '\\resources\\heatmap.html')