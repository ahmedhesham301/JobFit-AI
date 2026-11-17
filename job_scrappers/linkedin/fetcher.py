from scrapling.fetchers import Fetcher
from urllib.parse import urlencode


def fetch_jobs_page(title, location, seconds_old, offset):
    response = Fetcher.get(build_search_url(title, location, seconds_old, offset))
    return response


def build_search_url(title, location, seconds_old, start):
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    params = {
        "keywords": title,
        "location": location,
        "f_TPR": f"r{seconds_old}",
        "start": start,
    }
    query_string = urlencode(params, doseq=True)
    search_url = f"{base_url}?{query_string}"
    return search_url


def fetch_job_page(url):
    return Fetcher.get(url)
