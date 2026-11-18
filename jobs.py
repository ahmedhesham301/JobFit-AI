import himalayas.main as himalayas
import pandas as pd
import os
import utils
import job_scrappers.linkedin
import job_scrappers.wuzzuf
from job_scrappers.data import create_df

ENABLE_HIMALAYAS = os.getenv("himalayas", "").lower() == "true"


def getJobs(jobTitle, country, scrape_from):
    jobs = create_df()
    if ENABLE_HIMALAYAS:
        utils.print_search_msg(
            jobTitle, "himalayas", country, utils.get_seconds_old(scrape_from)
        )
        jobs = himalayas.scrape(jobTitle, utils.get_seconds_old(scrape_from), country)
        utils.print_found_jobs(jobTitle, "himalayas", country, jobs)
    return jobs


def scrape_linkedin(jobs, scrape_from):
    jobs_without_description = create_df()
    for job in jobs:
        df = job_scrappers.linkedin.scrape_jobs(
            job["role"], job["country"], utils.get_seconds_old(scrape_from), False
        )
        jobs_without_description = pd.concat(
            [jobs_without_description, df], ignore_index=True
        )
    return jobs_without_description


def scrape_wuzzuf(jobs):
    jobs_without_description = create_df()
    for job in jobs:
        df = job_scrappers.wuzzuf.scrape_jobs(job["role"], job["country"], False)
        jobs_without_description = pd.concat(
            [jobs_without_description, df], ignore_index=True
        )
    return jobs_without_description
