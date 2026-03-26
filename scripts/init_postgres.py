import psycopg2
import os

conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    category TEXT,
    action_type TEXT,
    reason TEXT,
    downtime FLOAT,
    impact_level TEXT,
    tags TEXT,
    system_name TEXT,
    created_by TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
conn.close()

print("Tables created")