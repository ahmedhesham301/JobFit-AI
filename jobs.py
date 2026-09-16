import jobspy
from jobspy import scrape_jobs
from jobspy.linkedin import LinkedIn


class _LinkedInWithOptionalSeniority(LinkedIn):
    """Work around python-jobspy 1.1.82 calling lower() on a missing level."""

    def _get_job_details(self, job_id: str) -> dict:
        details = super()._get_job_details(job_id)
        if details.get("job_level") is None:
            details["job_level"] = ""
        return details


# scrape_jobs builds its scraper mapping from this class on each call.
# Install once at import time, before concurrent searches start.
jobspy.LinkedIn = _LinkedInWithOptionalSeniority


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
        results_wanted=results_wanted,
        # google_search_term=f"{jobTitle} jobs near Cairo since {hours_old} hours",
        hours_old=hours_old,
        # JobSpy validates this even for LinkedIn-only searches.
        # LinkedIn uses location above to select the search country.
        country_indeed="worldwide",
        is_remote=is_remote,
        linkedin_fetch_description=True,  # gets more info such as description, direct job url (slower)
        # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
    )
    # print(jobs)
    return jobs
    # jobs.to_csv(
    #     "jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False
    # )  # to_excel
