from scrapling.fetchers import Fetcher
from urllib.parse import urlencode


def fetch_jobs_page(title, location, offset):
    response = Fetcher.get(build_search_url(title, location, offset))
    return response


def build_search_url(title: str, location: str, offset):
    base_url = f"https://bebee.com/{location}/jobs"
    params = {
        "q": title,
        # "postedWithin": "24h",
        "sort": "newest",
        "page": offset,
    }
    query_string = urlencode(params, doseq=True)
    search_url = f"{base_url}?{query_string}"
    return search_url


def fetch_job_page(url):
    return Fetcher.get(url)
