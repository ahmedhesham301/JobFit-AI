class Stats:
    def __init__(self):
        self.scraping_time = None
        self.language_filter_time = None
        self.filter_time = None
        self.email_time = None
        self.jobs_scraped_total = 0
        self.jobs_no_duplicates = 0
        self.jobs_no_description = 0
        self.descriptions_from_db = 0
        self.descriptions_scraped = 0
        self.jobs_dropped_no_description = 0
        self.jobs_skipped_by_title_filter = 0
        self.jobs_skipped_by_company_filter = 0
        self.jobs_skipped_by_description_language_filter = 0
        self.jobs_skipped_by_description_filter = 0
        self.jobs_skipped_by_positive_filter = 0
        self.cache_hits = 0
        self.total_jobs_rated = 0

    def format_summary(self):
        jobs_remaining = (
            self.jobs_no_duplicates
            - self.jobs_skipped_by_title_filter
            - self.jobs_skipped_by_company_filter
            - self.jobs_dropped_no_description
            - self.jobs_skipped_by_description_language_filter
            - self.jobs_skipped_by_description_filter
            - self.jobs_skipped_by_positive_filter
        )
        average_filter_time = (
            self.filter_time / self.jobs_no_duplicates
            if self.filter_time is not None and self.jobs_no_duplicates
            else None
        )
        rows = [
            ("Total jobs scraped", self.jobs_scraped_total),
            ("Unique jobs", self.jobs_no_duplicates),
            ("Jobs excluded by keyword filter", self.jobs_skipped_by_title_filter),
            ("Jobs excluded by company filter", self.jobs_skipped_by_company_filter),
            ("Jobs without description", self.jobs_no_description),
            ("Descriptions loaded from DB", self.descriptions_from_db),
            ("Descriptions scraped", self.descriptions_scraped),
            ("Jobs dropped (missing description)", self.jobs_dropped_no_description),
            (
                "Jobs excluded by description language filter",
                self.jobs_skipped_by_description_language_filter,
            ),
            (
                "Jobs excluded by description filter",
                self.jobs_skipped_by_description_filter,
            ),
            (
                "Jobs excluded by positive keyword filter",
                self.jobs_skipped_by_positive_filter,
            ),
            ("Jobs remaining after filtering", jobs_remaining),
            ("Jobs rated", self.total_jobs_rated),
            ("Cache hits", self.cache_hits),
            ("Scraping time", self.scraping_time),
            ("Language filtering time", self.language_filter_time),
            ("Filtering time", self.filter_time),
            ("Average filtering time per job", average_filter_time),
            ("Email time", self.email_time),
        ]
        label_width = max(len(label) for label, _ in rows)
        return "\n".join(
            ["Job search summary"]
            + [
                f"{label + ':':<{label_width + 2}}{value if value is not None else 'N/A'}"
                for label, value in rows
            ]
        )

    def print(self):
        print("\n" + self.format_summary())


s = Stats()
