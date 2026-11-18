from scrapling.fetchers import Fetcher
from urllib.parse import urlencode


def fetch_jobs_page(title, location, offset):
    response = Fetcher.get(build_search_url(title, location, offset))
    return response


def build_search_url(title, location, offset):
    base_url = "https://wuzzuf.net/search/jobs"
    params = {
        "q": title,
        "filters[country][0]": location,
        "filters[post_date][0]": "within_24_hours",
        "start": offset,
    }
    query_string = urlencode(params)
    return f"{base_url}?{query_string}"


def fetch_job_page(url):
    return Fetcher.get(url)
