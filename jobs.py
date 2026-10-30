from jobspy import scrape_jobs
import himalayas.main as himalayas
import pandas as pd
import os
import utils

ENABLE_HIMALAYAS = os.getenv("himalayas", "").lower() == "true"


def getJobs(jobTitle, results_wanted, country, is_remote, scrape_from):
    utils.print_search_msg(
        jobTitle, "linkedin", country, utils.get_seconds_old(scrape_from)
    )
    jobs = scrape_jobs(
        site_name=[
            # "indeed",
            "linkedin",
            # "zip_recruiter",
            # "google",
            # "glassdoor",
            # "bayt",
            # "naukri",
            # "bdjobs",
        ],
        search_term=jobTitle,
        location=country,
        country_indeed=country,
        results_wanted=results_wanted,
        # google_search_term=f"{jobTitle} jobs near Cairo since {hours_old} hours",
        hours_old=utils.get_seconds_old(scrape_from) / 3600,
        # JobSpy validates this even for LinkedIn-only searches.
        # LinkedIn uses location above to select the search country.
        is_remote=is_remote,
        fetch_description=True,
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
