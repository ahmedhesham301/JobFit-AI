import logging
import time
from ai import generate
import json
import sqlite3
from google.genai.errors import ServerError, ClientError
from httpx import RemoteProtocolError
import database
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

        description_id = database.insert_description(job["description"])
        evaluation_hash = database.get_evaluation_hash(job, cv)
        saved_info = database.get_info_from_hash(evaluation_hash)
        evaluation_id = saved_info["id"] if saved_info is not None else None
        if saved_info is not None:
            s.cache_hits += 1

        if rate and not saved_info:
            try_count = 3
            while try_count > 0:
                try:
                    logging.warning(f"index is {i}")
                    ai_response = generate(
                        job["title"], job["location"], job["description"], cv
                    )
                    ai_response_dict = json.loads(ai_response)

                    evaluation_id = database.insert_evaluation(
                        evaluation_hash, description_id, ai_response_dict
                    )
                    saved_info = database.get_info_from_hash(evaluation_hash)

                    break

                except (ValueError, KeyError, TypeError, sqlite3.IntegrityError) as e:
                    try_count -= 1
                    logging.warning("Invalid AI evaluation: %s", e)

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

        database.insert_job(job, evaluation_id=evaluation_id)

        if saved_info is not None and saved_info["percentage"] >= 60:
            good_fit_jobs.append(
                {
                    **saved_info,
                    "location": job.get("location"),
                    "title": job["title"],
                    "url": job["job_url"],
                    "why I'm I a good fit": saved_info["why_good_fit"],
                    "what I'm I missing": saved_info["what_is_missing"],
                    "percentage": saved_info["percentage"],
                }
            )
    return good_fit_jobs
