import concurrent.futures
import pandas as pd
from .linkedin.linkedin import scrape_job_details as scrape_linkedin_details
from .wuzzuf.wuzzuf import scrape_job_details as scrape_wuzzuf_details
from .bayt.bayt import scrape_job_details as scrape_bayt_details
from .bebee.bebee import scrape_job_details as scrape_bebee_details


def scrape_details(jobs: pd.DataFrame):
    linkedin_df = jobs[jobs["site"] == "linkedin"]
    wuzzuf_df = jobs[jobs["site"] == "wuzzuf"]
    bayt_df = jobs[jobs["site"] == "bayt"]
    bebee_df = jobs[jobs["site"] == "bebee"]
    other_df = jobs[~jobs["site"].isin(["linkedin", "wuzzuf", "bayt", "bebee"])]

    tasks = [
        (scrape_linkedin_details, linkedin_df),
        (scrape_wuzzuf_details, wuzzuf_df),
        (scrape_bayt_details, bayt_df),
        (scrape_bebee_details, bebee_df),
    ]

    dfs = [other_df]
    active_tasks = [(fn, df) for fn, df in tasks if not df.empty]
    if active_tasks:
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=len(active_tasks)
        ) as executor:
            futures = [executor.submit(fn, df) for fn, df in active_tasks]
            for future in concurrent.futures.as_completed(futures):
                dfs.append(future.result())

    return pd.concat(dfs, ignore_index=True)
