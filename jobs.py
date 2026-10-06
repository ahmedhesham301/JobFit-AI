import jobspy
from jobspy import scrape_jobs
from jobspy.linkedin import LinkedIn


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
        hours_old=hours_old,
        # JobSpy validates this even for LinkedIn-only searches.
        # LinkedIn uses location above to select the search country.
        is_remote=is_remote,
        fetch_description=True,
    )
    # print(jobs)
    return jobs
    # jobs.to_csv(
    #     "jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False
    # )  # to_excel
