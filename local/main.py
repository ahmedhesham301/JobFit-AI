import artifact_manger as am
import local_ai
import json
import pandas as pd
import time
from dotenv import load_dotenv
import alert
import os
import database
import vars
from status import Status

load_dotenv("/home/ahmed/Desktop/JobFit-AI/local/.env")

blacklist = [s.lower() for s in vars.blacklist]
db = database.Database()
status = Status()
start_time = time.perf_counter()
print(os.getenv("cv_path"))
with open(os.getenv("cv_path"), "r") as file:
    cv = file.read()

artifacts = am.list_artifacts("mokagad/job")["artifacts"]

print(f"Total artifacts: {len(artifacts)}")

# Inserts unfiltered jobs to database
# Does not insert jobs that are blacklisted in vars.py
for artifact in artifacts:
    if artifact["expired"] != True:
        df = am.get_an_artifact("mokagad/job", artifact["id"])
        print(f"Jobs to add to db: {len(df)}")
        for row in df.itertuples(index=False):
            if row.title.lower() not in blacklist: 
                db.insert_job(
                    row.job_url,
                    row.title,
                    row.description,
                    status
                )
            else:
                status.blacklisted_jobs += 1
        print("done")
    am.delete_artifact("mokagad/job", artifact["id"])

# Get jobs with same description and filter them
duplicated_descriptions = db.get_duplicated_descriptions()
for row in duplicated_descriptions:
    ai_response_json = local_ai.generate(row[0], cv)
    ai_response = json.loads(ai_response_json)
    if ai_response["fitPercentage"] >= 71:
        db.update_status_by_description(row[0], "good_fit_not_sent", ai_response["fitPercentage"],ai_response_json)
    else:
        db.update_status_by_description(row[0], "bad_fit", ai_response["fitPercentage"],ai_response_json)
    status.duplicates += row[1]
    print(f"jobs that is duplicated {row[1]} times\t{ai_response["fitPercentage"]}%")

# Get unfiltered individual jobs and filter them
unfiltered_jobs = db.get_jobs("unfiltered")
for row in unfiltered_jobs:
    ai_response_json = local_ai.generate(row[2], cv)
    print(ai_response_json)
    ai_response = json.loads(ai_response_json)
    if ai_response["fitPercentage"] >= 71:
        db.update_status_by_url(row[0], "good_fit_not_sent", ai_response["fitPercentage"], ai_response_json)
    else:
        db.update_status_by_url(row[0], "bad_fit", ai_response["fitPercentage"], ai_response_json)
    print(f"{row[1]}\t{ai_response["fitPercentage"]}%")


alert.send_email(
    os.getenv("smtp_email"),
    os.getenv("receiver_email"),
    os.getenv("smtp_password"),
    db.get_jobs("good_fit_not_sent"),
)
db.update_to_good_fit_sent()


end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.1f} seconds")
# print(f"Total jobs filtered: {total_jobs}")
status.print()
