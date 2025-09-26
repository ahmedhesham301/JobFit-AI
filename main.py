from jobs import getJobs
from ai import generate
from alert import send_email
import json
import time
import logging

SENDER = ""
PASSWORD = ""
RECEIVER = ""

good_fit_jobs = []


with open("instruction.txt", "r") as f:
    CV = f.read()


def get_jobs(job_title, cv, results_wanted, hours_old):
    jobs = getJobs(job_title, results_wanted, hours_old)
    for i, job in jobs.iterrows():
        # print(job["description"])
        # print("_______________")
        print("index is :", i)

        if (i + 1) % 10 == 0 and i != 0:
            print("Sleeping to avoid API rate limits")
            time.sleep(60)
        try_count = 3
        while try_count > 0:
                try:
                    cleaned_description = "\n".join(
                        [line for line in job["description"].splitlines() if line.strip()]
                    )
                    ai_response = generate(cleaned_description, cv)
                    ai_response_dict = json.loads(ai_response)
                    break
                except json.JSONDecodeError as e:
                    try_count -= 1
                    print("_______________")
                    print(cleaned_description)
                    print("_______________")
                    print(ai_response)
                    print(e)
                    print("Sleeping after fail to avoid API rate limits")
                    time.sleep(6)
        else:
            print("All attempts failed.")
            continue
        # print(ai_response_dict)
        if ai_response_dict["percentage"] > 0:
            # print("adding job to good_fit_jobs")
            good_fit_jobs.append(
                {
                    "title": job["title"],
                    "url": job["job_url"],
                    "percentage": ai_response_dict["percentage"],
                    "why I'm I a good fit": ai_response_dict["why I'm I a good fit"],
                    "what I'm I missing": ai_response_dict["what I'm I missing"],
                }
            )


if __name__ == "__main__":
    get_jobs("devops", CV, results_wanted=2, hours_old=4)
    # get_jobs("backend", CV, results_wanted=30, hours_old=2)
    if len(good_fit_jobs) > 0:
        send_email(SENDER, RECEIVER, PASSWORD, good_fit_jobs)
