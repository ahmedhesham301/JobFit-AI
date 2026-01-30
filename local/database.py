from psycopg_pool import ConnectionPool
from psycopg.errors import UniqueViolation


class Database:
    def __init__(self):
        self.pool = ConnectionPool("postgresql://postgres:1234@0.0.0.0:5432/postgres")

    def insert_job(self, url, title, description, status):
        try:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO jobs (url, title, description) VALUES (%s, %s, %s);",
                        (url, title, description),
                    )
        except UniqueViolation:
            status.duplicates += 1

    def update_status_by_url(self, url, status, percentage=None):
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
                cur.execute(
                    "SELECT * FROM jobs WHERE status = %s ORDER BY percentage DESC;",
                    (status,),
                )
                return cur.fetchall()

    def update_status_by_description(self, description, status, percentage=None):
        if percentage == None:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE jobs SET status = %s WHERE description = %s;",
                        (status, description),
                    )
        else:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE jobs SET status = %s, percentage = %s WHERE description = %s;",
                        (status, percentage, description),
                        prepare=True,
                    )

    def get_duplicated_descriptions(self):
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT description, COUNT(*) AS c
FROM (SELECT * FROM jobs WHERE status = 'unfiltered')
GROUP BY description
HAVING COUNT(*) > 1
ORDER BY c DESC;""",
                )
                return cur.fetchall()

    def update_to_good_fit_sent(self):
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE jobs SET status = 'good_fit_sent' WHERE status = 'good_fit_not_sent';"
                )
