from scrapling.fetchers import StealthyFetcher, Fetcher
from urllib.parse import urlencode

cookies = None

def solve_captha():
    url = "https://wuzzuf.net/jobs/egypt"
    response = StealthyFetcher.fetch(url, headless=True,solve_cloudflare=True)

    ALLOWED_COOKIES = {"cf_clearance", "countryIso", "language"}
    if isinstance(response.cookies, dict):
        cookies = response.cookies
    else:
        cookies = {c["name"]: c["value"] for c in response.cookies}

    print(cookies)
    
    return {
        "cf_clearance": cookies["cf_clearance"],
        "countryIso": cookies["countryIso"],
        "language": cookies["language"],
    }

    

def fetch_jobs_page(title, location, offset):
    global cookies
    if not cookies:
        cookies = solve_captha()
    response = Fetcher.get(build_search_url(title, location, offset), impersonate="chrome",cookies=cookies)
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
    return Fetcher.get(url, impersonate="chrome", cookies=cookies)

