from dotenv import load_dotenv

load_dotenv()

from rich.logging import RichHandler
from jobs import getJobs, scrape_linkedin, scrape_wuzzuf
from alert import send_email
from filter import filter_jobs, filter_jobs_by_regex, filter_jobs_by_language
import os
import logging
import pandas as pd
from stats import s
from datetime import datetime, timedelta, timezone
import concurrent.futures
from jobs_to_search import jobs
from math import ceil
import vars
import database
import utils
from ai import JobEvaluatorCache
from job_scrappers.data import create_df
from job_scrappers.main import scrape_details

logging.basicConfig(
    level=logging.WARNING,
    format=":%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
    force=True,
)
logging.getLogger("scrapling").propagate = False

SENDER = os.getenv("smtp_email")
PASSWORD = os.getenv("smtp_password")
RECEIVER = os.getenv("receiver_email")

all_jobs = create_df()
good_fit_jobs = []
with open("system_instruction.md", "r") as f:
    SYSTEM_INSTRUCTIONS = f.read()
with open("cv.txt", "r") as f:
    CV = f.read()


def main():
    global all_jobs, good_fit_jobs
    run_started_at = datetime.now(timezone.utc)
    previous_run_started_at = database.start_scrape_run(run_started_at)
    t = datetime.now()
    scrape_from = (
        previous_run_started_at
        if previous_run_started_at is not None
        else run_started_at - timedelta(hours=2)
    )

    linkedin_jobs_without_description = scrape_linkedin(jobs, scrape_from)
    wuzzuf_jobs_without_description = scrape_wuzzuf(jobs)
    all_jobs = pd.concat(
        [linkedin_jobs_without_description, wuzzuf_jobs_without_description],
        ignore_index=True,
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = []
        for index, job in enumerate(jobs):

            futures.append(
                executor.submit(getJobs, job["role"], job["country"], scrape_from)
            )
        for future in concurrent.futures.as_completed(futures):
            all_jobs = pd.concat([all_jobs, future.result()], ignore_index=True)
    s.jobs_scraped_total = len(all_jobs)
    s.scraping_time = datetime.now() - t

    if len(all_jobs) > 0:
        all_jobs = all_jobs.drop_duplicates(subset=["job_url"], ignore_index=True)
        s.jobs_no_duplicates = len(all_jobs)

        title_filtered_jobs, remaining = filter_jobs_by_regex(
            all_jobs, "title", vars.blocked_titles_regex
        )
        database.bulk_insert(remaining, "title_keyword_filter")
        s.jobs_skipped_by_title_filter = len(remaining)

        company_filtered_jobs, remaining = filter_jobs_by_regex(
            title_filtered_jobs, "company_name", vars.blocked_companies_regex
        )
        database.bulk_insert(remaining, "company_filter")
        s.jobs_skipped_by_company_filter = len(remaining)

        missing_before_db = int(company_filtered_jobs["description"].isna().sum())
        database.get_descriptions(company_filtered_jobs)
        jobs_with_description = scrape_details(company_filtered_jobs)
        # log how many jobs where dropped by next line
        missing_after_db = int(company_filtered_jobs["description"].isna().sum())

        missing_after_scrape = int(jobs_with_description["description"].isna().sum())
        jobs_with_description = jobs_with_description.dropna(subset=["description"])
        jobs_with_description["description"] = jobs_with_description[
            "description"
        ].apply(utils.clean_description)

        s.jobs_no_description = missing_before_db
        s.descriptions_from_db = missing_before_db - missing_after_db
        s.descriptions_scraped = missing_after_db - missing_after_scrape
        s.jobs_dropped_no_description = missing_after_scrape

        a = datetime.now()
        jobs_filtered_by_description_language, remaining = filter_jobs_by_language(
            jobs_with_description
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
        # The shared cache is created lazily when a job actually needs rating.
        cache = JobEvaluatorCache(SYSTEM_INSTRUCTIONS, CV)
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
                executor.submit(filter_jobs, chunk, SYSTEM_INSTRUCTIONS, CV, cache)
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
