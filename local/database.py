from psycopg_pool import ConnectionPool
from psycopg.errors import UniqueViolation


class Database:
    def __init__(self):
        self.pool = ConnectionPool("postgresql://postgres:1234@0.0.0.0:5432/postgres")

    def insert_job(self, url, title, description):
        try:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO jobs (url, title, description) VALUES (%s, %s, %s);",
                        (url, title, description),
                    )
        except UniqueViolation:
            pass

    def update_status(self, url, status, percentage=None):
        if percentage == None:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE jobs SET status = %s WHERE url = %s;", (status, url)
                    )
        else:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE jobs SET status = %s, percentage = %s WHERE url = %s;",
                        (status, percentage, url),
                        prepare=True,
                    )

    def get_jobs(self, status):
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM jobs WHERE status = %s", (status,))
                return cur.fetchall()
