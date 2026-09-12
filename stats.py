class Stats:
    def __init__(self):
        self.scraping_time = None
        self.filter_time = None
        self.email_time = None
        self.jobs_no_duplicates = 0
        self.jobs_duplicates = 0
        self.jobs_skipped_by_company_filter = 0
        self.jobs_skipped_by_keyword_filter = 0
        self.total_jobs_rated = 0

    def print(self):
        jobs_remaining = (
            self.jobs_no_duplicates
            - self.jobs_skipped_by_company_filter
            - self.jobs_skipped_by_keyword_filter
        )
        average_filter_time = (
            self.filter_time / self.jobs_no_duplicates
            if self.filter_time is not None and self.jobs_no_duplicates
            else None
        )
        rows = [
            ("Total jobs scraped", self.jobs_duplicates),
            ("Unique jobs with descriptions", self.jobs_no_duplicates),
            ("Jobs excluded by company filter", self.jobs_skipped_by_company_filter),
            ("Jobs excluded by keyword filter", self.jobs_skipped_by_keyword_filter),
            ("Jobs remaining after filtering", jobs_remaining),
            ("Jobs rated", self.total_jobs_rated),
            ("Scraping time", self.scraping_time),
            ("Filtering time", self.filter_time),
            ("Average filtering time per job", average_filter_time),
            ("Email time", self.email_time),
        ]
        label_width = max(len(label) for label, _ in rows)
        print("\nJob search summary")
        for label, value in rows:
            print(
                f"{label + ':':<{label_width + 2}}{value if value is not None else 'N/A'}"
            )


s = Stats()
