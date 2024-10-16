# This program is to create an R-Tree for spatial indexing
# This allows for easier access and creates bounding boxes which helps with targetting
import sqlite3
from rtree import index

# Step 1: Get the data from the sql database


def main():
    conn = sqlite3.connect("crime_data.db")
    print("Successfulyy connected to database")
    cursor = conn.cursor()

    # Use SQL commands to retrieve what I need
    query = "SELECT crime_index, LAT, LON FROM LA_Crime"
    cursor.execute(query)

    # Fetch all results from the query
    coordinates = cursor.fetchall() # This should give me the tuples

    # Let the program know where to save the R Tree
    r_tree_file = "r_tree_data_fixed"
    # Create an R-Tree Index
    rtree_index = index.Index(r_tree_file)

    # Insert data into the R-Tree
    for coordinate in coordinates:
        (id, lat, lon) = coordinate
        rtree_index.insert(id, (lon,lat,lon,lat))


    conn.close()

    print("R_Tree successfuly created and saved")

if __name__ == "__main__":
    main()
