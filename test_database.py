import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('crime_data.db')
cursor = conn.cursor()

# SQL query to find rows where either LAT or LON is 0.00
query = "SELECT * FROM LA_Crime WHERE LAT = 0 OR LON = 0"

# Execute the query
cursor.execute(query)

# Fetch all the rows where either LAT or LON is 0.00
rows_with_zero = cursor.fetchall()

# Print the number of rows found and the actual rows
print(f"Number of rows with LAT or LON as 0: {len(rows_with_zero)}")
for row in rows_with_zero:
    print(row)
query = "SELECT * FROM LA_Crime WHERE LAT IS NULL OR LON IS NULL"

# Execute the query
cursor.execute(query)

# Fetch all rows where LAT or LON is NULL
null_rows = cursor.fetchall()

# Check if any rows were returned
if null_rows:
    print(f"Found {len(null_rows)} rows where LAT or LON is NULL:")
    for row in null_rows:
        print(row)
else:
    print("No NULL values found in LAT or LON columns.")


delete_query = "DELETE FROM LA_CRIME WHERE LAT IS NULL OR LON IS NULL"

cursor.execute(delete_query)

conn.commit()

query = "SELECT * FROM LA_Crime WHERE LAT IS NULL OR LON IS NULL"

# Execute the query
cursor.execute(query)

# Fetch all rows where LAT or LON is NULL
null_rows = cursor.fetchall()

# Check if any rows were returned
if null_rows:
    print(f"Found {len(null_rows)} rows where LAT or LON is NULL:")
    for row in null_rows:
        print(row)
else:
    print("No NULL values found in LAT or LON columns.")

# Close the connection

conn.close()