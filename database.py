import os
import sqlite3

with sqlite3.connect(os.getenv("data_path"), timeout=30) as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        why_good_fit TEXT NOT NULL,
        what_missing TEXT NOT NULL,
        percentage INTEGER NOT NULL
    )
""")
    conn.execute("PRAGMA journal_mode=WAL")
