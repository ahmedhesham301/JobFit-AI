import pandas as pd
from .linkedin.linkedin import scrape_job_details as scrape_linkedin_details
from .wuzzuf.wuzzuf import scrape_job_details as scrape_wuzzuf_details
from .bayt.bayt import scrape_job_details as scrape_bayt_details


def scrape_details(jobs: pd.DataFrame):
    linkedin_df = jobs[jobs["site"] == "linkedin"]
    linkedin_with_details = scrape_linkedin_details(linkedin_df)

    wuzzuf_df = jobs[jobs["site"] == "wuzzuf"]
    wuzzuf_with_details = scrape_wuzzuf_details(wuzzuf_df)

    bayt_df = jobs[jobs["site"] == "bayt"]
    bayt_with_details = scrape_bayt_details(bayt_df)

    other_df = jobs[~jobs["site"].isin(["linkedin", "wuzzuf", "bayt"])]

    return pd.concat(
        [linkedin_with_details, wuzzuf_with_details, bayt_with_details, other_df],
        ignore_index=True,
    )
