import himalayas.main as himalayas
import pandas as pd
import utils
import job_scrappers.linkedin
import job_scrappers.wuzzuf
import job_scrappers.bayt
from job_scrappers.data import create_df
import time
from job_scrappers.data import COUNTRY_MAP


def scrape_linkedin(jobs, scrape_from):
    jobs_without_description = create_df()
    for job in jobs:
        df = job_scrappers.linkedin.scrape_jobs(
            job["role"], job["country"], utils.get_seconds_old(scrape_from), False
        )
        jobs_without_description = pd.concat(
            [jobs_without_description, df], ignore_index=True
        )
        time.sleep(0.5)
    return jobs_without_description


def scrape_himalayas(jobs, scrape_from):
    jobs_without_description = create_df()

    for job in jobs:
        df = himalayas.scrape(
            job["role"], utils.get_seconds_old(scrape_from), job["country"]
        )
        jobs_without_description = pd.concat(
            [jobs_without_description, df], ignore_index=True
        )
        # utils.print_found_jobs(jobTitle, "himalayas", country, jobs)
    return jobs_without_description


def scrape_wuzzuf(jobs):
    jobs_without_description = create_df()
    for job in jobs:
        df = job_scrappers.wuzzuf.scrape_jobs(job["role"], job["country"], False)
        jobs_without_description = pd.concat(
            [jobs_without_description, df], ignore_index=True
        )
    return jobs_without_description


def scrape_bayt(jobs):
    jobs_without_description = create_df()
    for job in jobs:
        df = job_scrappers.bayt.scrape_jobs(job["role"], job["country"], False)
        jobs_without_description = pd.concat(
            [jobs_without_description, df], ignore_index=True
        )
    return jobs_without_description
