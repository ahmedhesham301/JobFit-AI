import os
import sqlite3

with sqlite3.connect(os.getenv("data_path"), timeout=30) as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        description TEXT NOT NULL,
        why_good_fit TEXT,
        what_missing TEXT,
        percentage INTEGER,
        why_skipped TEXT
    )
""")
    conn.execute("PRAGMA journal_mode=WAL")

data_path = os.getenv("data_path")


def insert_job(
    title, url, description, why_good_fit, what_missing, percentage, why_skipped
):
    with sqlite3.connect(data_path, timeout=30) as conn:
        conn.execute(
            """
                        INSERT INTO jobs
                        (title, url, description, why_good_fit, what_missing, percentage, why_skipped)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
            (
                title,
                url,
                description,
                why_good_fit,
                what_missing,
                percentage,
                why_skipped,
            ),
        )


def bulk_insert(df, why_skipped):
    rows = (
        (title, url, description, None, None, None, why_skipped)
        for title, url, description in df[
            ["title", "job_url", "description"]
        ].itertuples(index=False, name=None)
    )
    with sqlite3.connect(data_path, timeout=30) as conn:
        conn.executemany(
            """
            INSERT INTO jobs
            (title, url, description, why_good_fit, what_missing, percentage, why_skipped)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
