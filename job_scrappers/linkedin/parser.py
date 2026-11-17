from ..data import create_df


def parse_job_cards(page):
    df = create_df()
    BASE_JOB_URL = "https://www.linkedin.com/jobs/view/"

    job_cards = page.css(".base-card")
    for job in job_cards:
        url = job.css(".base-card__full-link::attr(href)").get()
        if url:
            url = url.strip()

        title = job.css(".base-search-card__title::text").get()
        if title:
            title = title.strip()

        company_name = job.css("a.hidden-nested-link::text").get()
        if company_name:
            company_name = company_name.strip()

        company_url = job.css("a.hidden-nested-link::attr(href)").get()
        if company_url:
            company_url = company_url.strip()

        location = job.css(".job-search-card__location::text").get()
        if location:
            location = location.strip()

        date_posted = job.css(
            "time[class*='job-search-card__listdate']::attr(datetime)"
        ).get()

        if date_posted:
            date_posted = date_posted.strip()

        urn = job.css(".base-card::attr(data-entity-urn)").get()
        if urn:
            url = BASE_JOB_URL + urn.split(":")[-1]
        df.loc[len(df)] = {
            "site": "linkedin",
            "job_url": url,
            "title": title,
            "company_name": company_name,
            "company_url": company_url,
            "location": location,
            "date_posted": date_posted,
        }
    return df


def parse_job_details(job):
    details = {}

    # Extract full description text across nested tags
    description_parts = job.css("div.show-more-less-html__markup *::text").getall()
    details["description"] = " ".join(p.strip() for p in description_parts if p.strip())

    # Extract criteria items
    criterias = job.css(".description__job-criteria-list li")
    for c in criterias:
        header_text = c.css(".description__job-criteria-subheader::text").get()
        if not header_text:
            continue

        # Reassign stripped value
        header = header_text.strip()
        val_text = c.css("span.description__job-criteria-text--criteria::text").get()
        val = val_text.strip() if val_text else None

        if header == "Seniority level":
            details["job_level"] = val
        elif header == "Employment type":
            details["job_type"] = val
        elif header == "Industries":
            details["industry"] = val
        else:
            # print a warning
            pass

    return details
