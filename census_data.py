import sqlite3
import pandas as pd
import os 

# Read the excel file into a DataFrame
excel_file = os.path.join("..", "census.xlsx")
df = pd.read_excel(excel_file)


db_file = "crime_data.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()


table_name = "census_data"

df.to_sql(table_name, conn, if_exists = "replace", index=False)

conn.commit()
conn.close()

print("Loaded the table into the database")