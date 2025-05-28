import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('dht_data.db')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to retrieve all data from the readings table
cursor.execute("SELECT * FROM readings")

# Fetch all results
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the connection
conn.close()
