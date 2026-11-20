from scrapling.fetchers import StealthyFetcher


def solve_captcha(url, allowed_cookies):
    response = StealthyFetcher.fetch(url, headless=True, solve_cloudflare=True)

    # Sync User-Agent from StealthyFetcher to prevent Cloudflare 403 token mismatch
    headers = {}
    if hasattr(response, "request_headers") and response.request_headers:
        user_agent = response.request_headers.get(
            "user-agent"
        ) or response.request_headers.get("User-Agent")
        if user_agent:
            headers["User-Agent"] = user_agent

    if isinstance(response.cookies, dict):
        raw_cookies = response.cookies
    elif response.cookies:
        raw_cookies = {c["name"]: c["value"] for c in response.cookies}
    else:
        raw_cookies = {}

    # Safely filter only allowed cookies
    cookies = {k: raw_cookies[k] for k in allowed_cookies if k in raw_cookies}
    return cookies, headers
