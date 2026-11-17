from data import create_df
from scrapling.engines.toolbelt.custom import Response


def parse_job_cards(page: Response):
    df = create_df()
    BASE_JOB_URL = "https://wuzzuf.net"

    job_cards = page.css("div:has(> div > div > h2 > a)")

    for job in job_cards:
        # Job Title & URL
        title_el = job.css("h2 a").first
        title = title_el.get_all_text(strip=True)
        href = title_el.attrib.get("href", "").strip() if title_el else ""
        if href.startswith("http"):
            job_url = href
        elif href:
            job_url = f"{BASE_JOB_URL}{href}"
        else:
            job_url = None

        # Company Name & URL (handles both public and "Confidential" postings)
        meta_div = job.css("h2 ~ div").first
        company_el = meta_div.css("a").first if meta_div else None
        spans = meta_div.css("span") if meta_div else []

        if company_el and company_el.text:
            company_name = company_el.text.rstrip(" -").strip()
            company_url = company_el.attrib.get("href", "").strip() or None
            if company_url and company_url.startswith("/"):
                company_url = f"{BASE_JOB_URL}{company_url}"
            location_el = spans.first if spans else None
        else:
            company_url = None
            if len(spans) > 1:
                company_name = spans[0].text.rstrip(" -").strip()
                location_el = spans[1]
            elif spans:
                first_text = spans[0].text.strip()
                if "confidential" in first_text.lower():
                    company_name = first_text.rstrip(" -").strip()
                    location_el = None
                else:
                    company_name = None
                    location_el = spans[0]
            else:
                company_name = None
                location_el = None

        # Location & Date Posted
        location = (
            location_el.text.strip() if location_el and location_el.text else None
        )

        date_el = meta_div.xpath("./div").first if meta_div else None
        date_posted = date_el.text.strip() if date_el and date_el.text else None

        # Badges (job type & workplace)
        badges_div = job.css('div:has(> a[href*="-Jobs-"])').first
        info_div = (
            badges_div.xpath("./following-sibling::div[1]").first
            if badges_div
            else None
        )

        badges = (
            [s.text.strip() for s in badges_div.css("span") if s.text.strip()]
            if badges_div
            else []
        )
        job_type = ", ".join(badges) if badges else None

        job_level = None
        exp_years = None
        skills = []

        if info_div:
            level_el = info_div.css('a[href*="-Jobs-"]').first
            if level_el and level_el.text:
                job_level = level_el.text.strip().lstrip("·").strip()

            exp_el = info_div.xpath('.//span[contains(text(), "Exp")]').first
            if exp_el and exp_el.text:
                exp_years = exp_el.text.strip().lstrip("·").strip()

            for el in info_div.css("a, span"):
                t = el.text.strip().lstrip("·").strip()
                if not t or t == job_level or t == exp_years:
                    continue
                if t not in skills and not t.startswith("·"):
                    skills.append(t)

        df.loc[len(df)] = {
            "site": "wuzzuf",
            "job_url": job_url,
            "title": title,
            "company_name": company_name,
            "company_url": company_url,
            "location": location,
            "date_posted": date_posted,
            "job_type": job_type,
            "job_level": job_level,
            "skills": ", ".join(skills) if skills else None,
            "scraped_experience_years": exp_years,
        }
    return df


def parse_job_details(job: Response):
    details = {}
    section_titles = [
        "Internship Description",
        "Internship Requirements",
        "Job Description",
        "Job Requirements",
    ]
    sections = []
    for title in section_titles:
        matched_el = job.find_by_text(title, case_sensitive=False, first_match=True)
        if not matched_el:
            continue
        sections.append(matched_el.parent)

    description_parts = []
    for section in sections:
        description_parts.append(section.get_all_text("\n", True))
    description = "\n\n".join(description_parts)
    details["description"] = description

    return details
