from jobs import getJobs
from alert import send_email
from filter import filter_jobs
import os
import logging
from random import shuffle
import pandas as pd

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)

SENDER = os.getenv("smtp_email")
PASSWORD = os.getenv("smtp_password")
RECEIVER = os.getenv("receiver_email")
api_keys = os.getenv("api_keys").split(",")
shuffle(api_keys)

all_jobs = pd.DataFrame()
good_fit_jobs = []

with open("instruction.txt", "r") as f:
    CV = f.read()


def get_jobs(job_title, results_wanted, hours_old, country, location, is_remote):
    global all_jobs
    jobs = getJobs(job_title, results_wanted, hours_old, country, location, is_remote=False)
    all_jobs = pd.concat([all_jobs, jobs], ignore_index=True)


if __name__ == "__main__":
    get_jobs("devops", results_wanted=30, hours_old=2, country="egypt", location="cairo")
    get_jobs("backend", results_wanted=30, hours_old=2, country="egypt", location="cairo")
    get_jobs("software engineer",results_wanted=30,hours_old=2,country="egypt",location="cairo",)
    get_jobs("cloud", results_wanted=30, hours_old=2, country="egypt", location="cairo")
    get_jobs("site reliability engineer",results_wanted=30,hours_old=2,country="egypt",location="cairo")
    get_jobs("sre", results_wanted=30, hours_old=2, country="egypt", location="cairo")
    get_jobs("intern", results_wanted=30, hours_old=2, country="egypt", location="cairo")
    # get_jobs("devops",results_wanted=200,hours_old=2,country="worldwide",location="",is_remote=True)
    all_jobs.drop_duplicates(inplace=True, ignore_index=True)
    logging.warning(f"Total jobs no duplicates: {len(all_jobs)}")
    filter_jobs(all_jobs, CV, api_keys, good_fit_jobs)
    if len(good_fit_jobs) > 0:
        send_email(SENDER, RECEIVER, PASSWORD, good_fit_jobs)
    else:
        print("no good fit jobs")
