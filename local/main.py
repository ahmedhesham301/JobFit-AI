import artifact_manger as am
import local_ai
import json
import pandas as pd
import time
from dotenv import load_dotenv

load_dotenv()

start_time = time.perf_counter()

good_fit_jobs = pd.DataFrame(columns=["title", "description", "job_url", "percentage"])
bad_fit_jobs = pd.DataFrame(columns=["title", "description", "job_url", "percentage"])
total_jobs = 0

with open("local/cv.txt", "r") as file:
    cv = file.read()

artifacts = am.list_artifacts("mokagad/job")["artifacts"][0:3]

print(f"Total artifacts: {len(artifacts)}")

for artifact in artifacts:
    df = am.get_an_artifact("mokagad/job", artifact["id"])
    print(f"Jobs to filter: {len(df)}")
    total_jobs = total_jobs + len(df)
    for row in df.itertuples(index=False):
        ai_response = local_ai.generate(row.description, cv)
        ai_response = json.loads(ai_response)
        print(ai_response["fitPercentage"])
        if ai_response["fitPercentage"] < 70:
            bad_fit_jobs.loc[len(bad_fit_jobs)] = [
                row.title,
                row.description,
                row.job_url,
                ai_response["fitPercentage"]
            ]
        else:
            good_fit_jobs.loc[len(bad_fit_jobs)] = [
                row.title,
                row.description,
                row.job_url,
                ai_response["fitPercentage"],
            ]

for artifact in artifacts:
    am.delete_artifact("mokagad/job", artifact["id"])

good_fit_jobs.to_csv("goodfitjobs.csv")
bad_fit_jobs.to_csv("badfitjobs.csv")


end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.1f} seconds")
print(f"Total jobs filtered: {total_jobs}")
