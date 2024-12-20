import sqlite3
import pandas as pd

# Connect to the database (or create it)
conn = sqlite3.connect('database/head_hunter.db')
c = conn.cursor()

# Create the vacancies table
c.execute(
    """
    CREATE TABLE IF NOT EXISTS vacancies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        salary TEXT NOT NULL,
        experience TEXT NOT NULL,
        company TEXT NOT NULL,
        city TEXT NOT NULL
    )
    """
)

# Load data from CSV into a DataFrame
df = pd.read_csv('head_hunter.csv')

# Insert the DataFrame into the vacancies table, replacing existing data
df.to_sql('vacancies', conn, if_exists='replace', index=False)

# Commit changes and close the connection
conn.commit()
conn.close()
