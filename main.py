from jobs import getJobs
from alert import send_email
from filter import filter_jobs
import os
import logging
import pandas as pd
from key_manger import KeyManger
from stats import Stats
from datetime import datetime
import concurrent.futures
from jobs_to_search import jobs
from math import ceil

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)

SENDER = os.getenv("smtp_email")
PASSWORD = os.getenv("smtp_password")
RECEIVER = os.getenv("receiver_email")
api_keys = os.getenv("api_keys").split(",")

all_jobs = pd.DataFrame()
good_fit_jobs = []
km = KeyManger(api_keys)

with open("instruction.txt", "r") as f:
    CV = f.read()


def get_jobs(job):
    print(f"searching for {job["role"]}")
    jobs = getJobs(
        job["role"],
        job["results_wanted"],
        job["hours_old"],
        job["country"],
        job["city"],
        job["is_remote"],
    )
    return jobs


def main():
    global all_jobs, good_fit_jobs
    s = Stats()
    t = datetime.now()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_jobs, job) for job in jobs]
        for future in concurrent.futures.as_completed(futures):
            all_jobs = pd.concat([all_jobs, future.result()], ignore_index=True)

    s.scraping_time = datetime.now() - t

    s.jobs_duplicates = len(all_jobs)
    all_jobs.drop_duplicates(subset=["job_url"], inplace=True, ignore_index=True)
    all_jobs = all_jobs.dropna(subset=["description"])
    s.jobs_no_duplicates = len(all_jobs)
    t = datetime.now()
    jobs_per_chunk = ceil(len(all_jobs) / 5)
    jobs_chunks = [all_jobs[i : i + jobs_per_chunk] for i in range(0, len(all_jobs), jobs_per_chunk)]
    kms = km.split(len(jobs_chunks))
    print(f"number of jobs per chunk: {jobs_per_chunk}")
    print(f"number of job chunks: {len(jobs_chunks)}")
    print(f"number of kms: {len(kms)}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(filter_jobs, jobs_chunk, CV, km) for jobs_chunk,km in zip(jobs_chunks,kms)]
        for future in concurrent.futures.as_completed(futures):
            good_fit_jobs.extend(future.result())

    # all_api_key_used = filter_jobs(all_jobs, CV, km, good_fit_jobs)
    s.filter_time = datetime.now() - t
    if len(good_fit_jobs) > 0:
        t = datetime.now()
        send_email(SENDER, RECEIVER, PASSWORD, good_fit_jobs)
        s.email_time = datetime.now() - t
    else:
        logging.warning("no good fit jobs")

    s.end_time = datetime.now()
    s.print()

    # if all_api_key_used == True:
    #     return 429


if __name__ == "__main__":
    main()
