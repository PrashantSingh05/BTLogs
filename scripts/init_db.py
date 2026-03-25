import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "instance", "logs.db")

os.makedirs("instance", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 🔥 USERS TABLE (EMAIL BASED)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

# 🔥 LOGS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    category TEXT,
    action_type TEXT,
    reason TEXT,
    downtime REAL,
    impact_level TEXT,
    tags TEXT,
    system_name TEXT,
    created_by TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("✅ Database initialized with email-based users")