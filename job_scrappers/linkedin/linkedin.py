import pandas as pd
from ..data import create_df
from .fetcher import fetch_jobs_page, fetch_job_page
from .parser import parse_job_cards, parse_job_details
import time
import random
import logging


def scrape_job_details(jobs):
    jobs_no_duplicates = jobs.drop_duplicates(
        subset=["job_url"],
        ignore_index=True,
    )
    for job in jobs_no_duplicates.itertuples():
        # skip non linkedin jobs for safety
        if job.site != "linkedin":
            logging.error(
                "linkedin scrape_job_details function got called on a non linkedin job"
            )
            continue

        times_failed = 0
        while times_failed < 10:
            response = fetch_job_page(job.job_url)
            if response.status == 200:
                details = parse_job_details(response)
                jobs_no_duplicates.loc[job.Index, list(details.keys())] = list(
                    details.values()
                )
                times_failed = 0
                break
            elif response.status == 404:
                break
            elif response.status == 429:
                times_failed += 1
                sleep_time = random.randrange(300, 900, 1) / 100
                logging.warning(f"429: details page Sleeping for {sleep_time} seconds")
                time.sleep(sleep_time)
            else:
                times_failed += 1
                sleep_time = random.randrange(300, 900, 1) / 100
                logging.warning(
                    f"{response.status}: details page Sleeping for {sleep_time} seconds"
                )
                time.sleep(sleep_time)
    return jobs_no_duplicates


def scrape_jobs(
    title: str, location: str, seconds_old: int, fetch_details: bool = True
) -> pd.DataFrame:
    all_jobs_df = create_df()
    times_failed = 0
    offset = 0

    while True:
        page = fetch_jobs_page(title, location, seconds_old, offset)
        if page.status in [200]:
            page_jobs_df = parse_job_cards(page)
            all_jobs_df = pd.concat([all_jobs_df, page_jobs_df], ignore_index=True)
            if len(page_jobs_df) < 10:
                break
            offset += 10
            times_failed = 0
        elif page.status == 400:
            break
        elif page.status == 404:
            break
        elif page.status == 429:
            times_failed += 1
            if times_failed > 10:
                logging.warning(f"Got rate limited {times_failed} times skipping")
                break
            sleep_time = random.randrange(300, 900, 1) / 100
            logging.warning(f"429 jobs page Sleeping for {sleep_time} seconds")
            time.sleep(sleep_time)
        else:
            logging.critical(f"Got {page.status}")
            break

    if not fetch_details:
        return all_jobs_df

    jobs_with_descriptions = scrape_job_details(all_jobs_df)
    return jobs_with_descriptions
