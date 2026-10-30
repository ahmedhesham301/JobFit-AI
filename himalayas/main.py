import time

import requests
import pandas as pd
import os
import logging

URL = "https://himalayas.app/jobs/api/search"
COLUMNS = [
    "site",
    "title",
    "company",
    "location",
    "job_type",
    "interval",
    "min_amount",
    "max_amount",
    "job_url",
    "description",
]


# scrape
def scrape(jobTitle, seconds_old, country):
    df = pd.DataFrame(columns=COLUMNS)
    epoch_seconds = int(time.time() - seconds_old)
    # build params
    query_params = {"q": jobTitle, "sort": "recent", "page": 1}
    if country == "worldwide":
        query_params["worldwide"] = True
    else:
        query_params["country"] = country

    tries = 3
    while tries:
        response = requests.get(
            URL,
            params=query_params,
            headers={"Authorization": f"Bearer {os.getenv("himalayas_api_key")}"},
            timeout=10,
        )
        if response.status_code == 200:
            jobs = response.json()["jobs"]
            if len(jobs) == 0:
                return df
            for job in jobs:
                if job["pubDate"] < epoch_seconds:
                    return df
                new_row = pd.DataFrame(
                    [
                        {
                            "site": "himalayas",
                            "title": job["title"],
                            "company": job["companyName"],
                            "location": "TODO",
                            "job_type": job["employmentType"],
                            "interval": job["salaryPeriod"],
                            "min_amount": job["minSalary"],
                            "max_amount": job["maxSalary"],
                            "job_url": job["applicationLink"],
                            "description": job["description"],
                        }
                    ]
                )
                df = pd.concat([df, new_row], ignore_index=True)
            query_params["page"] += 1
        elif response.status_code in [429, 503]:
            print(response.headers)
            sleep_time = int(response.headers.get("Retry-After", "60"))
            print(f"himalayas rate limit hit sleeping for {sleep_time} seconds")
            time.sleep(sleep_time)
            tries -= 1
        elif response.status_code == 401:
            logging.critical("got 401 response from himalayas api", response.text)
            return df
        else:
            print(f"Error {response.status_code}: {response.text}")
            tries -= 1
    else:
        logging.critical("himalayas all tries failed")
        return df


# pd.set_option("display.max_colwidth", None)
# data = scarpe("devops", 3000, "worldwide")
# print(data["JOB_URL"])
