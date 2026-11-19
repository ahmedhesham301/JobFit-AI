from urllib.parse import urlencode
from scrapling.fetchers import Fetcher
from ..utils import solve_captcha

cookies = None
headers = None

ALLOWED_COOKIES = {"cf_clearance", "countryIso", "language"}


def fetch_jobs_page(title, location, offset):
    global cookies, headers
    if not cookies:
        cookies, headers = solve_captcha(
            "https://wuzzuf.net/jobs/egypt", ALLOWED_COOKIES
        )

    response = Fetcher.get(
        build_search_url(title, location, offset),
        impersonate="chrome",
        cookies=cookies,
        headers=headers,
    )
    return response


def fetch_job_page(url):
    global cookies, headers
    if not cookies:
        cookies, headers = solve_captcha(
            "https://wuzzuf.net/jobs/egypt", ALLOWED_COOKIES
        )

    return Fetcher.get(
        url,
        impersonate="chrome",
        cookies=cookies,
        headers=headers,
    )


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
