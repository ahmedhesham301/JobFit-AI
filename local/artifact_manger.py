import requests
import zipfile
import io
import pandas as pd
from os import getenv

GITHUB_TOKEN = getenv("gh_token")

def list_artifacts(repo):
    url = f"https://api.github.com/repos/{repo}/actions/artifacts"
    headers = {
    "accept": "application/vnd.github+json",
    "per_page": "100",
    "X-GitHub-Api-Version": "2022-11-28",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    }
    response = requests.get(url, headers=headers)
    return(response.json())

def get_an_artifact(repo, artifact_id):
    url = f"https://api.github.com/repos/{repo}/actions/artifacts/{artifact_id}/zip"
    headers = {
        "accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }
    response = requests.get(url, headers=headers)
    with io.BytesIO(response.content) as zipped_file:
        with zipfile.ZipFile(zipped_file, 'r') as archive:
            with archive.open("output.csv") as data_file:
                content = data_file.read().decode("utf-8")
                jobs_df = pd.read_csv(io.StringIO(content))
                return jobs_df


def delete_artifact(repo, artifact_id):
    url = f"https://api.github.com/repos/{repo}/actions/artifacts/{artifact_id}"
    headers = {
        "accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }
    response = requests.delete(url,headers=headers)
    if response.status_code == 204:
        return
    else:
        # TODO raise error
        print("error at delete function :" + response.text)


# print(list_artifacts("mokagad/job"))
# get_an_artifact("mokagad/job", 5163872934)
