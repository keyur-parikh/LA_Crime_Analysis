# The job of this program is to convert the excel file into sqlite program
import pandas as pd
import sqlite3 
import os

excel_file = os.path.join("..", "Crime_Data_Recleaned.xlsx")

# Read the excel file into a data frame
df = pd.read_excel(excel_file)

# Connect to Sqlite database

conn = sqlite3.connect("crime_data.db")
cursor = conn.cursor()

# Convert the dataframe into a sqlite table

df.to_sql("LA_Crime", conn, if_exists = "replace", index = True)

# Commit changes and close
conn.commit()
conn.close()

print("Successfuly converted into a sqlite3 database")