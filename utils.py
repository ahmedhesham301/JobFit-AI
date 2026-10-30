import hashlib
from datetime import datetime, timezone
from math import ceil


def hash_text(text: str):
    return hashlib.sha256(text.encode()).hexdigest()


def clean_description(description):
    if not isinstance(description, str):
        return ""

    cleaned = "\n".join(
        line for line in description.replace("\\", "").splitlines() if line.strip()
    )

    return " ".join(cleaned.lower().split())


def get_seconds_old(scrape_from):
    # Convert the fixed cutoff when this search starts, including any queue delay.
    # JobSpy's LinkedIn filter uses seconds; round up to avoid narrowing the window.
    seconds_old = max(
        1, ceil((datetime.now(timezone.utc) - scrape_from).total_seconds())
    )
    return seconds_old


def print_search_msg(title, website, country, seconds_old):
    hours, minutes = divmod(seconds_old // 60, 60)
    print(
        f"searching for job {title} for the past {hours}:{minutes:02d} "
        f"in {country} "
        f"on {website}"
    )


def print_found_jobs(job_title, website, country, df):
    summary = (
        f"\nRole: {job_title}\n"
        f"Country: {country}\n"
        f"Website: {website}\n"
        f"Found {len(df)} jobs\n"
        f"{'-' * 50}\n"
    )
    # JobSpy can return an empty DataFrame without any columns.
    if not df.empty:
        summary += "\n".join(
            f"  {i}. {title}" for i, title in enumerate(df["title"], start=1)
        )
    print(summary + "\n")
