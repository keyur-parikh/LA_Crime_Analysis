# First, I am going to have access to coordinates that I need 

import sqlite3
from r_tree import index
import math
import numpy as np
from geopy.distance import distance
from opencage.geocoder import OpenCageGeocode


def get_zip_code(coordinates):
    # got this code from the api website
    lat,lon = coordinates

    key = "373e3a30e326478799562f8de2ac6a1c"

    geocoder = OpenCageGeocode(key)
    
    results = geocoder.reverse_geocode(lat, lon)

    postcode = results[0]["components"].get("postcode", "No postcode found")

    return postcode

def get_population_density(coordinates):

    postcode = get_zip_code(coordinates)

    # Connect to the database
    db_file = "crime_data.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    query = 'SELECT "Total Population" FROM census_data WHERE "Zip Code" = ?'

    cursor.execute(query, (postcode, ))

    population = cursor.fetchone()

    conn.close()

    if population:
        return population[0]
    else:
        return None





def haversine(lat1, lon1, lat2, lon2):
    """This calculates the true distance between the points and is a more reliable
    than just using bounding boxes"""
    # Convert degrees to radians
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)
    
    # Differences between latitudes and longitudes
    dLat = lat2 - lat1
    dLon = lon2 - lon1
    
    # Haversine formula
    a = np.sin(dLat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dLon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    # Radius of Earth in kilometers
    rad = 3958.8
    
    # Calculate distance
    return rad * c

def get_bounding_box(coordinate, radius):
    lat, lon = coordinate

    # Calculate the four corners of the bounding box
    lat_min = distance(miles=radius).destination((lat,lon),bearing = 180).latitude
    lat_max = distance(miles=radius).destination((lat,lon),bearing = 0).latitude
    lon_min = distance(miles=radius).destination((lat,lon),bearing = 270).longitude
    lon_max = distance(miles=radius).destination((lat,lon),bearing = 90).longitude

    return lat_min, lon_min, lat_max, lon_max

def get_intersection(coordinate, radius):
    """This takes in input as the coordinate of desire
    and finds all the points that are in the interested bounding box
    Returns: All the indexes in the bounding box that can be used in the database"""
    lat, lon = coordinate
    r_tree_file = "r_tree_data_fixed"
    db_file = "crime_data.db"

    #Connect to the database
    conn = sqlite3.connect(db_file)
    print("Succesfully connected to database")
    cursor = conn.cursor()

    r_tree_index = index.Index(r_tree_file)
    # This is to get the range and since 69 miles is 1 degree we divide it by 69
    # Then we get the max and min interval by adding and subtracting the range
    #lat_range = radius / 69
    #lon_range = radius / (69 * math.cos(math.radians(lat)))

    #min_lat = lat - lat_range
    #max_lat = lat + lat_range
    #min_lon = lon - lon_range
    #max_lon = lon + lon_range
    min_lat, min_lon, max_lat, max_lon = get_bounding_box(coordinate, radius)
    # Query the R-tree with longitude comes first and then the latitide
    possible_points = list(r_tree_index.intersection((min_lon,min_lat,max_lon,max_lat)))

    if not possible_points:
        return []
    
    batch_size = 900
    all_data = []
    for i in range(0, len(possible_points), batch_size):
        batch = possible_points[i:i+batch_size]
        query = f"SELECT crime_index, LAT, LON FROM LA_Crime WHERE crime_index IN ({','.join('?'for _ in batch)})"
        cursor.execute(query, batch)
        all_data.extend(cursor.fetchall())

    # Convert data into numpy arrays for haversine
    #print(len(all_data))
    data = np.array(all_data)
    #print(data)

    ids = data[:, 0]
    latitudes = data[:, 1].astype(float)
    longitudes = data[:, 2].astype(float)

    distances = haversine(lat, lon, latitudes, longitudes)

    # Filter based on the radius
    within_radius = ids[distances <= radius]

    conn.close()

    return within_radius


coordinate1 = (34.0522, -118.2437)
coordinate3 = (33.8968, -118.2201)
coordinate2 = (36.1699, -115.1398)
coordinate4 = (33.9432, -118.2435)
radius = 5


result1 = get_intersection(coordinate1, radius)
result2 = get_intersection(coordinate2, radius)
result3 = get_intersection(coordinate3, radius)
result4 = get_intersection(coordinate4, radius)

pop1 = get_population_density(coordinate1)
pop2 = get_population_density(coordinate2)
pop3 = get_population_density(coordinate3)
pop4 = get_population_density(coordinate4)

print("LA Population", pop1)
print("Watts Population", pop4)
print("Compton Population", pop3)


print("Length of the LA one", len(result1)/pop1)
print("Length of Compton One", len(result3)/pop3)
print("Length of the Watts One", len(result4)/pop4)



