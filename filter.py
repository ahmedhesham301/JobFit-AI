import logging
import time
from ai import generate
import json
from google.genai.errors import ServerError, ClientError
from httpx import RemoteProtocolError

total_fail = 0
total_overload = 0
total_fail_overload = 0
total_empty_response = 0
total_fail_empty_response = 0


def filter_jobs(jobs, cv, km, good_fit_jobs):
    global total_fail,total_overload,total_fail_overload,total_empty_response,total_fail_empty_response

    for i, job in jobs.iterrows():
        # print("index is :", i)  # for debugging
        try_count = 3
        while try_count > 0:

            try:
                logging.warning(f"index is {i}")
                cleaned_description = "\n".join(
                    [line for line in job["description"].splitlines() if line.strip()]
                )
                ai_response = generate(cleaned_description, cv, km.get_key())
                ai_response_dict = json.loads(ai_response)
                break

            except json.JSONDecodeError as e:
                try_count -= 1
                total_empty_response += 1
                if try_count == 0:
                    total_fail += 1
                    total_fail_empty_response += 1

                logging.warning("JSONDecodeError happend")

            except ServerError as e:

                if e.details["error"]["code"] == 503:
                    try_count -= 1
                    total_overload += 1
                    if try_count == 0:
                        total_fail += 1
                        total_fail_overload += 1
                    logging.warning("sleeping to after The model is overloaded.")
                    time.sleep(3)
                else:
                    logging.critical(e.details)
                    return 1

            except ClientError as e:
                if e.details["error"]["code"] == 429:
                    logging.exception("api limit hit")
                    if km.delete_key() == 1:
                        return 429
                    logging.warning(f"total api keys count after deleting current key: {len(km.keys)}")
                    time.sleep(10)
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

        if ai_response_dict["percentage"] > 70:
            good_fit_jobs.append(
                {
                    "title": job["title"],
                    "url": job["job_url"],
                    "percentage": ai_response_dict["percentage"],
                    "why I'm I a good fit": ai_response_dict["why I'm I a good fit"],
                    "what I'm I missing": ai_response_dict["what I'm I missing"],
                }
            )
    print_stats
    return good_fit_jobs


def print_stats():
    stats = f"""total fail: {total_fail}
total empty responses: {total_empty_response} fail: {total_fail_empty_response}
Total overloads:       {total_overload}       fail: {total_fail_overload}"""
    logging.warning(stats)
