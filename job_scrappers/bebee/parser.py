import json
from scrapling.parser import Adaptor
from ..data import create_df


def parse_job_cards(page):
    df = create_df()
    BASE_JOB_URL = "https://bebee.com"

    job_cards = page.css("article[data-voice-job='card']") or page.css("article")
    for job in job_cards:
        # Title & Job URL
        title_el = job.css("h3 a").first
        title = title_el.get_all_text(strip=True) if title_el else None
        if not title:
            title = job.attrib.get("data-voice-title", "").strip() or None

        href = title_el.attrib.get("href", "").strip() if title_el else ""
        if not href:
            href = job.attrib.get("data-voice-url", "").strip()

        if href.startswith("http"):
            job_url = href
        elif href:
            job_url = f"{BASE_JOB_URL}{href}"
        else:
            job_url = None

        # Company Name & URL
        company_el = job.css('a[href*="/companies/"]').first
        if company_el:
            company_name = company_el.get_all_text(strip=True) or None
            href = company_el.attrib.get("href", "").strip()
            if href.startswith("http"):
                company_url = href
            elif href:
                company_url = f"{BASE_JOB_URL}{href}"
            else:
                company_url = None
        else:
            company_url = None
            company_span = job.css("span.truncate").first
            company_name = (
                company_span.get_all_text(strip=True)
                if company_span
                else job.attrib.get("data-voice-company", "").strip() or None
            )

        # Job Type (employment type & workplace badges)
        badge_spans = job.css("span.rounded-full")
        badges = [
            s.get_all_text(strip=True)
            for s in badge_spans
            if s.get_all_text(strip=True)
        ]
        job_type = ", ".join(badges) if badges else None

        # Date Posted
        clock_svg = job.css("svg.lucide-clock").first
        if clock_svg and clock_svg.parent:
            date_posted = clock_svg.parent.get_all_text(strip=True) or None
        else:
            date_posted = None

        df.loc[len(df)] = {
            "site": "bebee",
            "job_url": job_url,
            "title": title,
            "company_name": company_name,
            "company_url": company_url,
            "location": None,
            "date_posted": date_posted,
            "job_type": job_type,
        }
    return df


def parse_job_details(job):
    if isinstance(job, str):
        job = Adaptor(job)

    details = {}

    # 1. Parse JSON-LD JobPosting if present
    json_ld = {}
    scripts = job.css("script[type='application/ld+json']")
    for s in scripts:
        try:
            if hasattr(s, "json"):
                data = s.json()
            elif hasattr(s, "text") and s.text:
                data = json.loads(s.text)
            else:
                data = None
            if isinstance(data, dict) and data.get("@type") == "JobPosting":
                json_ld = data
                break
        except Exception:
            pass

    # 2. Location
    location = None
    pin_svg = job.css("svg.lucide-map-pin").first
    if pin_svg and pin_svg.parent:
        location = pin_svg.parent.get_all_text(strip=True) or None
    if not location:
        voice_el = job.css("[data-voice-job='detail']").first
        if voice_el:
            location = voice_el.attrib.get("data-voice-location", "").strip() or None
    if not location and json_ld.get("jobLocation"):
        addr = json_ld["jobLocation"].get("address", {})
        loc = addr.get("addressLocality")
        country = addr.get("addressCountry")
        if loc and country:
            location = f"{loc}, {country}"
        elif loc:
            location = loc
    details["location"] = location

    # 3. Description
    description = None
    desc_el = job.css("[data-voice-description]").first or job.css("div.prose").first
    if desc_el:
        description = desc_el.get_all_text("\n", strip=True) or None
    if not description and json_ld.get("description"):
        description = (
            Adaptor(json_ld["description"]).get_all_text("\n", strip=True) or None
        )
    details["description"] = description

    # 4. Job Type (employment type & workplace)
    job_type = None
    detail_first_div = job.css("[data-voice-job='detail'] > div").first
    if detail_first_div:
        badges = [
            s.get_all_text(strip=True)
            for s in detail_first_div.css("span.rounded-xl")
            if s.get_all_text(strip=True)
        ]
        if badges:
            job_type = ", ".join(badges)
    if not job_type and json_ld.get("employmentType"):
        job_type = json_ld["employmentType"]
    details["job_type"] = job_type

    # 5. Industry
    industry = None
    tag_svg = job.css("svg.lucide-tag").first
    if tag_svg and tag_svg.parent:
        industry = tag_svg.parent.get_all_text(strip=True) or None
    if not industry and json_ld.get("industry"):
        industry = json_ld["industry"]
    details["industry"] = industry

    # 6. Skills
    skills = None
    skill_spans = job.css("span.bg-muted\\/60")
    if skill_spans:
        skills_list = [
            s.get_all_text(strip=True)
            for s in skill_spans
            if s.get_all_text(strip=True)
        ]
        if skills_list:
            skills = ", ".join(skills_list)
    if not skills and json_ld.get("skills"):
        skills = json_ld["skills"]
    details["skills"] = skills

    # 7. Scraped Experience Years
    scraped_experience_years = None
    months = json_ld.get("experienceRequirements", {}).get("monthsOfExperience")
    if months:
        years = months // 12
        scraped_experience_years = (
            f"{years}+ years" if years > 0 else f"{months} months"
        )
    details["scraped_experience_years"] = scraped_experience_years

    # 8. Date Posted (prefer JSON-LD datePosted, fallback to DOM clock icon)
    date_posted = json_ld.get("datePosted")
    if not date_posted:
        clock_svg = job.css("svg.lucide-clock").first
        if clock_svg and clock_svg.parent:
            date_posted = clock_svg.parent.get_all_text(strip=True) or None
    details["date_posted"] = date_posted

    return details
