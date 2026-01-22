import artifact_manger as am
import local_ai
import json
import pandas as pd
import time
from dotenv import load_dotenv
import alert
import os
import database
load_dotenv(".env")

db = database.Database()

start_time = time.perf_counter()

with open("cv.txt", "r") as file:
    cv = file.read()

artifacts = am.list_artifacts("mokagad/job")["artifacts"]

print(f"Total artifacts: {len(artifacts)}")

# Inserts unfiltered jobs to database
for artifact in artifacts:
    if artifact["expired"] != True:
        df = am.get_an_artifact("mokagad/job", artifact["id"])
        print(f"Jobs to add to db: {len(df)}")
        for row in df.itertuples(index=False):
            db.insert_job(
                row.job_url,
                row.title,
                row.description,
            )
    am.delete_artifact("mokagad/job", artifact["id"])

# Get unfiltered jobs and filter them
unfiltered_jobs = db.get_jobs("unfiltered")
for row in unfiltered_jobs:
    ai_response = local_ai.generate(row[2], cv)
    ai_response = json.loads(ai_response)
    if ai_response["fitPercentage"] >= 65:
        db.update_status(row[0], "good_fit_not_sent", ai_response["fitPercentage"])
    else:
        db.update_status(row[0], "bad_fit", ai_response["fitPercentage"])
    print(f"{row[1]}\t{ai_response["fitPercentage"]}%")


alert.send_email(
    os.getenv("smtp_email"),
    os.getenv("receiver_email"),
    os.getenv("smtp_password"),
    db.get_jobs("good_fit_not_sent"),
)


end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.1f} seconds")
# print(f"Total jobs filtered: {total_jobs}")
