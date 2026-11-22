import pandas as pd


def create_df():
    return pd.DataFrame(
        columns=[
            "site",
            "job_url",
            "title",
            "company_name",
            "company_url",
            "location",
            "job_type",
            "job_level",
            "scraped_experience_years",
            "description",
            "skills",
            "why_skipped",
            "industry",
            "date_posted",
            "discovered_at",
            "sent_at",
            "times_sent",
        ]
    )


COUNTRY_MAP = {
    "worldwide": {"gulftalent": ""},
    "egypt": {
        "linkedin": "egypt",
        "wuzzuf": "Egypt",
        "bayt": "egypt",
        "gulftalent": "10229362000000",
        "bebee": "eg",
    },
}
