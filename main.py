from jobs import getJobs
from alert import send_email
from filter import filter_jobs
import os
import logging
import pandas as pd
from stats import Stats
from datetime import datetime
import concurrent.futures
from jobs_to_search import jobs
from math import ceil
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)

SENDER = os.getenv("smtp_email")
PASSWORD = os.getenv("smtp_password")
RECEIVER = os.getenv("receiver_email")
api_key = os.getenv("gemini_api_key")

all_jobs = pd.DataFrame()
good_fit_jobs = []
with open("instruction.txt", "r") as f:
    CV = f.read()


def get_jobs(job):
    print(f"searching for {job["role"]} past {job["hours_old"]} hours\n")
    jobs = getJobs(
        job["role"],
        job["results_wanted"],
        job["hours_old"],
        job["country"],
        job["city"],
        job["is_remote"],
    )
    for _, job in jobs.iterrows():
        print(f"{job["title"]}\n")

    return jobs


def main():
    global all_jobs, good_fit_jobs
    s = Stats()
    t = datetime.now()
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = [executor.submit(get_jobs, job) for job in jobs]
        for future in concurrent.futures.as_completed(futures):
            all_jobs = pd.concat([all_jobs, future.result()], ignore_index=True)

    s.scraping_time = datetime.now() - t

    s.jobs_duplicates = len(all_jobs)
    all_jobs.drop_duplicates(subset=["job_url"], inplace=True, ignore_index=True)
    all_jobs = all_jobs.dropna(subset=["description"])
    s.jobs_no_duplicates = len(all_jobs)
    t = datetime.now()
    if len(all_jobs) > 0:
        num_chunks = max(1, 5)
        jobs_per_chunk = ceil(len(all_jobs) / num_chunks)
        jobs_chunks = [
            all_jobs[i : i + jobs_per_chunk]
            for i in range(0, len(all_jobs), jobs_per_chunk)
        ]
        print(f"number of jobs per chunk: {jobs_per_chunk}")
        print(f"number of job chunks: {len(jobs_chunks)}")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(filter_jobs, chunk, CV, api_key)
                for chunk in jobs_chunks
            ]
            for future in concurrent.futures.as_completed(futures):
                good_fit_jobs.extend(future.result())

    s.filter_time = datetime.now() - t
    if len(good_fit_jobs) > 0:
        t = datetime.now()
        send_email(SENDER, RECEIVER, PASSWORD, good_fit_jobs)
        s.email_time = datetime.now() - t
    else:
        logging.warning("no good fit jobs")

    s.end_time = datetime.now()
    s.print()


if __name__ == "__main__":
    main()
