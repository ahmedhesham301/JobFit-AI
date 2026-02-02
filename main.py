from jobs import getJobs
import os
import logging
import pandas as pd
from stats import Stats
from datetime import datetime,timedelta
import concurrent.futures
from jobs_to_search import jobs
import json

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)

SENDER = os.getenv("smtp_email")
PASSWORD = os.getenv("smtp_password")
RECEIVER = os.getenv("receiver_email")
api_keys = os.getenv("api_keys").split(",")
workflow_runs_info = json.loads(os.getenv("last_run_info"))

all_jobs = pd.DataFrame()
good_fit_jobs = []
last_run_info = None
with open("instruction.txt", "r") as f:
    CV = f.read()

if len(workflow_runs_info) == 2:
    if workflow_runs_info[1]["conclusion"] == "success":
        last_run_info = datetime.strptime(workflow_runs_info[1]["createdAt"], "%Y-%m-%dT%H:%M:%SZ")

def get_jobs(job, last_run_info):
    if last_run_info == None:
        last_run_info = datetime.now() - timedelta(hours=job["hours_old"])

    diff = datetime.now() - last_run_info
    hours_old = diff.total_seconds() / 3600
    if hours_old > 4:
        hours_long = job["hours_old"]
    else:
        hours_long = hours_old
    hours, remainder = divmod(hours_long , 1)
    minutes = remainder * 60
    print(f"searching for {job["role"]} past {int(hours)}:{int(minutes)} hours")
    jobs = getJobs(
        job["role"],
        job["results_wanted"],
        hours_long,
        job["country"],
        job["city"],
        job["is_remote"],
    )
    return jobs
def clean_description(d):
    cleaned_description = "\n".join(
        [line for line in d.splitlines() if line.strip()]
    )
    return cleaned_description

def main():
    global all_jobs, good_fit_jobs
    s = Stats()
    t = datetime.now()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(get_jobs, job,last_run_info) for job in jobs]
        for future in concurrent.futures.as_completed(futures):
            all_jobs = pd.concat([all_jobs, future.result()], ignore_index=True)

    s.scraping_time = datetime.now() - t

    s.jobs_duplicates = len(all_jobs)
    all_jobs.drop_duplicates(subset=["job_url"], inplace=True, ignore_index=True)
    all_jobs = all_jobs.dropna(subset=["description"])
    s.jobs_no_duplicates = len(all_jobs)
    all_jobs = all_jobs[["title", "description", "job_url", "company", "city"]]
    all_jobs["description"] = all_jobs["description"].apply(clean_description)
    all_jobs.to_csv("/output/output.csv", index=False)

    s.print()


if __name__ == "__main__":
    main()
