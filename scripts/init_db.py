import sqlite3
from app.config import Config

def init_db():
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'pending'
    )
    """)

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

    # Create Admin (your credentials)
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO users (username, password, role)
        VALUES ('admin', 'adminlogs', 'admin')
        """)

    conn.commit()
    conn.close()
    print("DB ready with admin/adminlogs")

if __name__ == "__main__":
    init_db()