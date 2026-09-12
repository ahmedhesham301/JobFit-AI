import logging
import time
from ai import generate
import json
from google.genai.errors import ServerError, ClientError
from httpx import RemoteProtocolError
import database
import vars
from stats import s


def filter_jobs(jobs, cv):
    good_fit_jobs = []
    for i, job in jobs.iterrows():
        if job["company"].lower() in vars.companies_blacklist:
            logging.warning(f"companies filter index {i} skipped {job["title"]}")
            database.insert_job(
                job["title"], job["job_url"], None, None, None, "company"
            )
            s.jobs_skipped_by_company_filter += 1
            continue
        if any(
            keyword in job["title"].lower() for keyword in vars.title_key_word_blacklist
        ):
            logging.warning(f"keywords filter index {i} skipped {job['title']}")
            database.insert_job(
                job["title"], job["job_url"], None, None, None, "keyword"
            )
            s.jobs_skipped_by_keyword_filter += 1
            continue

        try_count = 3
        while try_count > 0:
            try:
                logging.warning(f"index is {i}")
                cleaned_description = "\n".join(
                    [line for line in job["description"].splitlines() if line.strip()]
                )
                ai_response = generate(cleaned_description, cv)
                ai_response_dict = json.loads(ai_response)
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
        database.insert_job(
            job["title"],
            job["job_url"],
            ai_response_dict["why I'm I a good fit in summary"],
            ai_response_dict["what I'm I missing in summary"],
            ai_response_dict["percentage"],
            None,
        )
        s.total_jobs_rated += 1

        if ai_response_dict["percentage"] > 70:
            good_fit_jobs.append(
                {
                    "title": job["title"],
                    "url": job["job_url"],
                    "percentage": ai_response_dict["percentage"],
                    "why I'm I a good fit": ai_response_dict[
                        "why I'm I a good fit in summary"
                    ],
                    "what I'm I missing": ai_response_dict[
                        "what I'm I missing in summary"
                    ],
                }
            )
    return good_fit_jobs
