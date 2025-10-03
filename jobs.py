from jobspy import scrape_jobs
import logging


def getJobs(
    jobTitle,
    results_wanted,
    hours_old,
    country,
    location,
    is_remote,
):
    jobs = scrape_jobs(
        site_name=[
            "indeed",
            "linkedin",
            # "zip_recruiter",
            # "google",
            # "glassdoor",
            # "bayt",
            # "naukri",
            # "bdjobs",
        ],
        search_term=jobTitle,
        location=location,
        results_wanted=results_wanted,
        # google_search_term=f"{jobTitle} jobs near Cairo since {hours_old} hours",
        hours_old=hours_old,
        country_indeed=country,
        is_remote=is_remote,
        linkedin_fetch_description=True,  # gets more info such as description, direct job url (slower)
        # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
    )
    logging.warning(f"Found {len(jobs)} {jobTitle} jobs in {location},{country}")
    # print(jobs)
    return jobs
    # jobs.to_csv(
    #     "jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False
    # )  # to_excel
