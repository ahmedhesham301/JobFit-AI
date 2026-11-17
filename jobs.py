import himalayas.main as himalayas
import pandas as pd
import os
import utils
import job_scrappers.linkedin
from job_scrappers.data import create_df

ENABLE_HIMALAYAS = os.getenv("himalayas", "").lower() == "true"


def getJobs(jobTitle, country, scrape_from):
    utils.print_search_msg(
        jobTitle, "linkedin", country, utils.get_seconds_old(scrape_from)
    )
    # linkedin
    jobs = job_scrappers.linkedin.scrape_jobs(
        jobTitle, country, utils.get_seconds_old(scrape_from), True
    )

    utils.print_found_jobs(jobTitle, "linkedin", country, jobs)
    if ENABLE_HIMALAYAS:
        utils.print_search_msg(
            jobTitle, "himalayas", country, utils.get_seconds_old(scrape_from)
        )
        jobs2 = himalayas.scrape(jobTitle, utils.get_seconds_old(scrape_from), country)
        utils.print_found_jobs(jobTitle, "himalayas", country, jobs2)
        jobs = pd.concat([jobs, jobs2], ignore_index=True)
    # print(jobs)
    return jobs
    # jobs.to_csv(
    #     "jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False
    # )  # to_excel
