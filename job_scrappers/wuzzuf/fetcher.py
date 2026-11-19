from urllib.parse import urlencode
from scrapling.fetchers import Fetcher, StealthyFetcher

cookies = None
user_agent = None

ALLOWED_COOKIES = {"cf_clearance", "countryIso", "language", "uid"}


def solve_captcha(force: bool = False):
    global cookies, user_agent
    if cookies and not force:
        return cookies

    url = "https://wuzzuf.net/jobs/egypt"
    response = StealthyFetcher.fetch(url, headless=True, solve_cloudflare=True)

    # Sync User-Agent from StealthyFetcher to prevent Cloudflare 403 token mismatch
    if hasattr(response, "request_headers") and response.request_headers:
        user_agent = response.request_headers.get("user-agent") or response.request_headers.get("User-Agent")

    if isinstance(response.cookies, dict):
        raw_cookies = response.cookies
    elif response.cookies:
        raw_cookies = {c["name"]: c["value"] for c in response.cookies}
    else:
        raw_cookies = {}

    # Safely filter only allowed cookies
    cookies = {k: raw_cookies[k] for k in ALLOWED_COOKIES if k in raw_cookies}
    return cookies


# Backward compatibility alias
solve_captha = solve_captcha


def get_headers():
    headers = {}
    if user_agent:
        headers["User-Agent"] = user_agent
    return headers


def fetch_jobs_page(title, location, offset):
    global cookies
    if not cookies:
        solve_captcha()

    response = Fetcher.get(
        build_search_url(title, location, offset),
        impersonate="chrome",
        cookies=cookies,
        headers=get_headers(),
    )
    return response


def fetch_job_page(url):
    global cookies
    if not cookies:
        solve_captcha()

    return Fetcher.get(
        url,
        impersonate="chrome",
        cookies=cookies,
        headers=get_headers(),
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
