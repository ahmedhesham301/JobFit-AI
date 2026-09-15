import logging
import time
from ai import generate
import json
from google.genai.errors import ServerError, ClientError
from httpx import RemoteProtocolError
import database
import vars
from stats import s
import os

rate = os.getenv("rate") == "true"


def filter_jobs_by_regex(jobs, key, regex):
    mask = jobs[key].str.contains(
        regex,
        case=False,
        regex=True,
        na=False,
    )

    skipped = jobs[mask].copy()
    remaining = jobs[~mask].copy()

    return remaining, skipped


def filter_jobs(jobs, cv):
    """Save filtered jobs, optionally rating eligible jobs with Gemini."""
    good_fit_jobs = []
    for i, job in jobs.iterrows():
        job = job.to_dict()

        saved_info = database.get_info_from_hash(job["description_hash"])
        if saved_info is not None:
            s.cache_hits += 1
            job["why I'm I a good fit"] = saved_info["why_good_fit"]
            job["what I'm I missing"] = saved_info["what_missing"]
            job["percentage"] = saved_info["percentage"]

        if rate and not saved_info:
            try_count = 3
            while try_count > 0:
                try:
                    logging.warning(f"index is {i}")
                    ai_response = generate(job["description"], cv)
                    ai_response_dict = json.loads(ai_response)

                    job["why I'm I a good fit"] = ai_response_dict[
                        "why I'm I a good fit in summary"
                    ]
                    job["what I'm I missing"] = ai_response_dict[
                        "what I'm I missing in summary"
                    ]
                    job["percentage"] = ai_response_dict["percentage"]

                    database.insert_hash(
                        job["description_hash"],
                        job["why I'm I a good fit"],
                        job["what I'm I missing"],
                        job["percentage"],
                    )

                    break

                except json.JSONDecodeError as e:
                    try_count -= 1
                    logging.warning("JSONDecodeError happend")

                except ServerError as e:

                    if e.details["error"]["code"] == 503:
                        try_count -= 1
                        logging.warning("sleeping to after The model is overloaded.")
                        time.sleep(3)
                    else:
                        logging.critical(e.details)
                        return 1

                except ClientError as e:
                    if (
                        e.details["error"]["code"] == 429
                        and e.details["error"]["status"] == "RESOURCE_EXHAUSTED"
                    ):
                        logging.error("RESOURCE_EXHAUSTED sleeping for 60 seconds")
                        time.sleep(60)
                    else:
                        logging.critical(e.details)
                        return 1

                except RemoteProtocolError as e:
                    try_count -= 1
                    logging.exception("sleeping after RemoteProtocolError")
                    time.sleep(3)

            else:
                logging.critical("All attempts failed")
                continue

            s.total_jobs_rated += 1

        job["description_id"] = database.insert_hash(
            job["description_hash"],
            job.get("why I'm I a good fit in summary"),
            job.get("what I'm I missing in summary"),
            job.get("percentage"),
        )
        database.insert_job(
            job["title"],
            job["job_url"],
            job["description"],
            job["is_remote"],
            job["description_id"],
            None,
        )

        if job.get("percentage") is not None and job.get("percentage") > 70:
            good_fit_jobs.append(
                {
                    "title": job["title"],
                    "url": job["job_url"],
                    "why I'm I a good fit": job["why I'm I a good fit"],
                    "what I'm I missing": job["what I'm I missing"],
                    "percentage": job["percentage"],
                }
            )
    return good_fit_jobs
