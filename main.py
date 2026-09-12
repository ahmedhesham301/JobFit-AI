from dotenv import load_dotenv

load_dotenv()

from jobs import getJobs
from alert import send_email
from filter import filter_jobs, filter_jobs_by_regex
import os
import logging
import pandas as pd
from stats import s
from datetime import datetime
import concurrent.futures
from jobs_to_search import jobs
from math import ceil
import vars
import database

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)

SENDER = os.getenv("smtp_email")
PASSWORD = os.getenv("smtp_password")
RECEIVER = os.getenv("receiver_email")

all_jobs = pd.DataFrame()
good_fit_jobs = []
with open("instruction.txt", "r") as f:
    CV = f.read()


def get_jobs(job_info):
    print(
        f"searching for {job_info["role"]} past {job_info["hours_old"]} hours in {job_info["country"]}\n"
    )
    jobs = getJobs(
        job_info["role"],
        job_info["results_wanted"],
        job_info["hours_old"],
        job_info["country"],
        job_info["city"],
        job_info["is_remote"],
    )
    summary = (
        f"\nRole: {job_info['role']}\n"
        f"Country: {job_info['country']}\n"
        f"Found {len(jobs)} jobs\n"
        f"{'-' * 50}\n"
    )
    summary += "\n".join(
        f"  {i}. {title}" for i, title in enumerate(jobs["title"], start=1)
    )
    print(summary + "\n")
    return jobs


def main():
    global all_jobs, good_fit_jobs
    t = datetime.now()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(get_jobs, job) for job in jobs]
        for future in concurrent.futures.as_completed(futures):
            all_jobs = pd.concat([all_jobs, future.result()], ignore_index=True)

    s.scraping_time = datetime.now() - t

    if len(all_jobs) > 0:
        s.jobs_duplicates = len(all_jobs)
        all_jobs.drop_duplicates(subset=["job_url"], inplace=True, ignore_index=True)
        all_jobs = all_jobs.dropna(subset=["description"], ignore_index=True)
        s.jobs_no_duplicates = len(all_jobs)

        # TODO insert the skipped jobs to db
        title_filtered_jobs, remaining = filter_jobs_by_regex(all_jobs, "title", vars.blocked_titles_regex)
        database.bulk_insert(remaining,"title")
        s.jobs_skipped_by_title_filter = len(remaining)

        company_filtered_jobs, remaining = filter_jobs_by_regex(title_filtered_jobs, "company", vars.blocked_companies_regex)
        database.bulk_insert(remaining,"company")
        s.jobs_skipped_by_company_filter = len(remaining)

        description_filtered_jobs, remaining = filter_jobs_by_regex(company_filtered_jobs, "description", vars.blocked_descriptions_regex)
        database.bulk_insert(remaining,"description")
        s.jobs_skipped_by_description_filter = len(remaining)

        print(f"Total jobs to filter: {len(description_filtered_jobs)}")

        t = datetime.now()

        num_chunks = 5
        jobs_per_chunk = max(1, ceil(len(description_filtered_jobs) / num_chunks))
        jobs_chunks = [
            description_filtered_jobs[i : i + jobs_per_chunk]
            for i in range(0, len(description_filtered_jobs), jobs_per_chunk)
        ]
        print(f"number of jobs per chunk: {jobs_per_chunk}")
        print(f"number of job chunks: {len(jobs_chunks)}")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(filter_jobs, chunk, CV) for chunk in jobs_chunks]
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
