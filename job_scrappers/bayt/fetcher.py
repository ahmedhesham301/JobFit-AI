from scrapling.fetchers import Fetcher
from ..utils import solve_captcha

cookies = None
headers = None

ALLOWED_COOKIES = {"cf_clearance"}


def fetch_jobs_page(title, location, offset):
    global cookies, headers
    if not cookies:
        cookies, headers = solve_captcha(
            "https://www.bayt.com/en/egypt/", ALLOWED_COOKIES
        )

    response = Fetcher.get(
        build_search_url(title, location, offset),
        impersonate="chrome",
        cookies=cookies,
        headers=headers,
    )
    return response


def build_search_url(title, location, offset):
    search_url = f"https://www.bayt.com/en/{location}/jobs/{title.replace(" ", "-")}-jobs/?filters%5bjb_last_modification_date_interval%5d%5b%5d=3&options%5Bsort%5D%5B%5D=d&page={offset}"
    return search_url


def fetch_job_page(url):
    global cookies, headers
    if not cookies:
        cookies, headers = solve_captcha(
            "https://www.bayt.com/en/egypt/", ALLOWED_COOKIES
        )
    return Fetcher.get(url, impersonate="chrome", cookies=cookies, headers=headers)
