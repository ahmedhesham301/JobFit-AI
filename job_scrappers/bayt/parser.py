from ..data import create_df
from scrapling.engines.toolbelt.custom import Response


def parse_job_cards(page: Response):
    df = create_df()
    BASE_JOB_URL = "https://www.bayt.com"

    job_cards = page.css("li[data-js-job]")

    for job in job_cards:
        # Job Title & URL
        title_el = job.css("h2 a").first
        title = title_el.get_all_text(strip=True) if title_el else None
        href = title_el.attrib.get("href", "").strip() if title_el else ""
        if href.startswith("http"):
            job_url = href
        elif href:
            job_url = f"{BASE_JOB_URL}{href}"
        else:
            job_url = None

        # Company Name & URL
        company_el = job.css("div.job-company-location-wrapper div a").first
        if company_el:
            company_name = company_el.get_all_text(" ", strip=True)
            company_url = company_el.attrib.get("href", "").strip() or None
            if company_url and company_url.startswith("/"):
                company_url = f"{BASE_JOB_URL}{company_url}"
        else:
            company_name = None
            company_url = None

        # Location
        location_el = job.css("dt.jb-label-location")
        if location_el:
            location = location_el.first.get_all_text(strip=True)
        else:
            location = None

        # Date Posted
        date_el = job.css("span[data-automation-id='job-active-date']").first
        date_posted = date_el.text.strip() if date_el and date_el.text else None

        df.loc[len(df)] = {
            "site": "bayt",
            "job_url": job_url,
            "title": title,
            "company_name": company_name,
            "company_url": company_url,
            "location": location,
            "date_posted": date_posted,
        }
    return df


def parse_job_details(job: Response):
    details = {}

    description_el = job.css('[data-jb-field="description"]').first
    if description_el:
        details["description"] = description_el.get_all_text("\n", strip=True)
    else:
        details["description"] = None

    industry_el = job.css('[data-automation-id="id_company_employees_industry"]').first
    if industry_el:
        details["industry"] = industry_el.get_all_text(strip=True)
    remote_el = job.css('[data-automation-id="id_remote_working"]').first
    if remote_el:
        details["job_type"] = remote_el.get_all_text(strip=True)

    return details
