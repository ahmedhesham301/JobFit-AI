from dotenv import load_dotenv

load_dotenv()

from jobs import getJobs
from alert import send_email
from filter import filter_jobs, filter_jobs_by_regex, filter_jobs_by_language
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
import utils
from ai import create_job_evaluator_cache

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)

SENDER = os.getenv("smtp_email")
PASSWORD = os.getenv("smtp_password")
RECEIVER = os.getenv("receiver_email")

all_jobs = pd.DataFrame()
good_fit_jobs = []
with open("system_instruction.md", "r") as f:
    SYSTEM_INSTRUCTIONS = f.read()
with open("cv.txt", "r") as f:
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
    # JobSpy can return an empty DataFrame without any columns.
    if not jobs.empty:
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

        title_filtered_jobs, remaining = filter_jobs_by_regex(
            all_jobs, "title", vars.blocked_titles_regex
        )
        database.bulk_insert(remaining, "title_keyword_filter")
        s.jobs_skipped_by_title_filter = len(remaining)

        company_filtered_jobs, remaining = filter_jobs_by_regex(
            title_filtered_jobs, "company", vars.blocked_companies_regex
        )
        database.bulk_insert(remaining, "company_filter")
        s.jobs_skipped_by_company_filter = len(remaining)

        company_filtered_jobs["description"] = company_filtered_jobs[
            "description"
        ].apply(utils.clean_description)

        a = datetime.now()

        jobs_filtered_by_description_language, remaining = filter_jobs_by_language(
            company_filtered_jobs
        )
        database.bulk_insert(remaining, "description_language")
        s.jobs_skipped_by_description_language_filter = len(remaining)

        s.language_filter_time = datetime.now() - a

        jobs_filtered_by_description_keyword, remaining = filter_jobs_by_regex(
            jobs_filtered_by_description_language,
            "description",
            vars.blocked_descriptions_regex,
        )
        database.bulk_insert(remaining, "description_keyword_filter")
        s.jobs_skipped_by_description_filter = len(remaining)

        remaining, positive_filtered_jobs = filter_jobs_by_regex(
            jobs_filtered_by_description_keyword,
            "description",
            vars.positive_keywords_regex,
        )
        database.bulk_insert(remaining, "positive_keyword_filter")
        s.jobs_skipped_by_positive_filter = len(remaining)

        positive_filtered_jobs["description_hash"] = None

        positive_filtered_jobs["description_hash"] = positive_filtered_jobs[
            "description"
        ].apply(utils.hash_text)

        print(f"Total jobs to filter: {len(positive_filtered_jobs)}")

        t = datetime.now()
        # TODO: clean this mess
        # if rate is disabled filter_jobs crashes because cache_name is undeclared
        # TODO: Create cache only if it is needed
        if os.getenv("rate") == "true":
            cache_name = create_job_evaluator_cache(
                SYSTEM_INSTRUCTIONS,
                CV,
            )
        else:
            cache_name = "bla"
        num_chunks = 5
        jobs_per_chunk = max(1, ceil(len(positive_filtered_jobs) / num_chunks))
        jobs_chunks = [
            positive_filtered_jobs[i : i + jobs_per_chunk]
            for i in range(0, len(positive_filtered_jobs), jobs_per_chunk)
        ]
        print(f"number of jobs per chunk: {jobs_per_chunk}")
        print(f"number of job chunks: {len(jobs_chunks)}")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(filter_jobs, chunk, SYSTEM_INSTRUCTIONS, CV, cache_name)
                for chunk in jobs_chunks
            ]
            for future in concurrent.futures.as_completed(futures):
                good_fit_jobs.extend(future.result())

    s.filter_time = datetime.now() - t
    if len(good_fit_jobs) > 0:
        t = datetime.now()
        send_email(SENDER, RECEIVER, PASSWORD, good_fit_jobs, s.format_summary())
        database.mark_jobs_sent(job["url"] for job in good_fit_jobs)
        s.email_time = datetime.now() - t
    else:
        logging.warning("no good fit jobs")

    s.end_time = datetime.now()
    s.print()


if __name__ == "__main__":
    main()
