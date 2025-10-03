import sqlite3

# Create SQLite DB and table
conn = sqlite3.connect("sample.db")
cursor = conn.cursor()

# Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    signup_date DATE
);
""")

# Insert some sample data
cursor.executemany("""
INSERT INTO users (name, signup_date) VALUES (?, ?)
""", [
    ("Alice", "2025-09-20"),
    ("Bob", "2025-09-25"),
    ("Charlie", "2025-09-28")
])

conn.commit()
conn.close()
