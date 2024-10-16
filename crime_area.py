from rtree import index
import math

r_tree_file = "r_tree_data_fixed"

r_tree_index = index.Index(r_tree_file)

parent_bounds = r_tree_index.bounds
min_lon, min_lat, max_lon, max_lat = parent_bounds

print(parent_bounds)

avg_lat = (min_lat + max_lat) / 2
width_km = (max_lon - min_lon) * 111 * math.cos(math.radians(avg_lat))

height_km = (max_lat - min_lat) * 111

area_km2 = width_km * height_km
print(area_km2)