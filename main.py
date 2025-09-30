from jobs import getJobs
from ai import generate
from google.genai.errors import ServerError, ClientError
from alert import send_email
import json
import time
import os
import logging
from random import shuffle

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)

SENDER = os.getenv("smtp_email")
PASSWORD = os.getenv("smtp_password")
RECEIVER = os.getenv("receiver_email")
api_keys = os.getenv("api_keys").split(",")

good_fit_jobs = []

# stats
total_fail = 0
total_fail_overload = 0
total_overload = 0
total_empty_response = 0
total_fail_empty_response = 0

shuffle(api_keys)

with open("instruction.txt", "r") as f:
    CV = f.read()


def get_jobs(job_title, cv, results_wanted, hours_old):
    global total_fail, total_fail_overload, total_overload, total_empty_response, total_fail_empty_response
    key_number = 0

    jobs = getJobs(job_title, results_wanted, hours_old)
    for i, job in jobs.iterrows():
        print("index is :", i)  # for debugging

        if (i + 1) % 10 == 0 and i != 0:
            logging.warning("sleeping to avoid API rate limits")
            time.sleep(60)
        try_count = 3

        while try_count > 0:

            try:
                cleaned_description = "\n".join(
                    [line for line in job["description"].splitlines() if line.strip()]
                )
                ai_response = generate(cleaned_description, cv, api_keys[key_number])
                ai_response_dict = json.loads(ai_response)
                break

            except json.JSONDecodeError as e:
                try_count -= 1
                total_empty_response += 1
                if try_count == 0:
                    total_fail += 1
                    total_fail_empty_response += 1

                logging.warning("Sleeping after JSONDecodeError")
                time.sleep(6)

            except ServerError as e:

                if e.details["error"]["code"] == 503:
                    try_count -= 1
                    total_overload += 1
                    if try_count == 0:
                        total_fail += 1
                        total_fail_overload += 1
                    logging.warning("sleeping to after The model is overloaded.")
                    print(e.details)
                    time.sleep(10)
                else:
                    logging.critical(e.details)
                    return 1

            except ClientError as e:
                if e.details["error"]["code"] == 429:
                    logging.warning("api limit hit")
                    key_number += 1
                    if key_number > len(api_keys) - 1:
                        logging.critical("All api keys hit the limit")
                        return 1
                else:
                    logging.critical(e.details)
                    return 1

        else:
            logging.critical("All attempts failed")
            continue

        if ai_response_dict["percentage"] > 50:
            good_fit_jobs.append(
                {
                    "title": job["title"],
                    "url": job["job_url"],
                    "percentage": ai_response_dict["percentage"],
                    "why I'm I a good fit": ai_response_dict["why I'm I a good fit"],
                    "what I'm I missing": ai_response_dict["what I'm I missing"],
                }
            )


def print_stats():
    stats = f"""total fail: {total_fail}
total empty responses: {total_empty_response} fail: {total_fail_empty_response}
Total overloads:       {total_overload}       fail: {total_fail_overload}"""
    print(stats)


if __name__ == "__main__":
    get_jobs("devops", CV, results_wanted=30, hours_old=2)
    get_jobs("backend", CV, results_wanted=30, hours_old=2)
    get_jobs("software engineer", CV, results_wanted=30, hours_old=2)
    if len(good_fit_jobs) > 0:
        send_email(SENDER, RECEIVER, PASSWORD, good_fit_jobs)
    else:
        print("no good fit jobs")
    print_stats()
