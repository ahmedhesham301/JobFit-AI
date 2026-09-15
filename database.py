import os
import sqlite3

with sqlite3.connect(os.getenv("data_path"), timeout=30) as conn:
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS descriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description_hash TEXT UNIQUE NOT NULL,
        why_good_fit TEXT,
        what_missing TEXT,
        percentage INTEGER
    );

    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        description TEXT NOT NULL,
        is_remote BOOLEAN NOT NULL,
        description_id INTEGER,
        why_skipped TEXT,
        FOREIGN KEY (description_id) REFERENCES descriptions(id)
    );
""")


data_path = os.getenv("data_path")


def insert_job(title, url, description, is_remote,description_id, why_skipped):
    with sqlite3.connect(data_path, timeout=30) as conn:
        conn.execute(
            """
            INSERT INTO jobs
            (title, url, description, is_remote, description_id, why_skipped)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                url,
                description,
                is_remote,
                description_id,
                why_skipped,
            ),
        )


def bulk_insert(df, why_skipped):
    rows = (
        (title, url, description, is_remote, why_skipped)
        for title, url, description, is_remote in df[
            ["title", "job_url", "description", "is_remote"]
        ].itertuples(index=False, name=None)
    )
    with sqlite3.connect(data_path, timeout=30) as conn:
        conn.executemany(
            """
            INSERT INTO jobs
            (title, url, description, is_remote, why_skipped)
            VALUES (?, ?, ?, ?, ?)
            """,
            rows,
        )


def insert_hash(description_hash, why_good_fit, what_missing, percentage):
    with sqlite3.connect(data_path, timeout=30) as conn:
        row = conn.execute(
            """
            INSERT INTO descriptions
                (description_hash, why_good_fit, what_missing, percentage)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(description_hash) DO NOTHING
            RETURNING id
            """,
            (
                description_hash,
                why_good_fit,
                what_missing,
                percentage,
            ),
        ).fetchone()

        # If inserted, RETURNING gives us the ID
        if row:
            return row[0]

        # If it already existed, get its existing ID
        row = conn.execute(
            """
            SELECT id
            FROM descriptions
            WHERE description_hash = ?
            """,
            (description_hash,),
        ).fetchone()

        return row[0]


def get_info_from_hash(description_hash):
    with sqlite3.connect(data_path, timeout=30) as conn:
        row = conn.execute(
            """
            SELECT why_good_fit, what_missing, percentage
            FROM descriptions
            WHERE description_hash = ?
            """,
            (description_hash,),
        ).fetchone()

    if not row:
        return None

    return {
        "why_good_fit": row[0],
        "what_missing": row[1],
        "percentage": row[2],
    }
