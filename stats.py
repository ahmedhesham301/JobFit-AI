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
        print(f"""Total jobs with duplicates: {self.jobs_duplicates}
Total jobs no duplicates: {self.jobs_no_duplicates}
Jobs skipped by companies filter: {self.jobs_skipped_by_company_filter}
Jobs skipped by keyword filter: {self.jobs_skipped_by_keyword_filter}
Total jobs rated: {self.total_jobs_rated}
Scraping time: {self.scraping_time}
Filter_time: {self.filter_time if self.jobs_no_duplicates else "N/A"}
AVG request time: {self.filter_time / self.jobs_no_duplicates if self.jobs_no_duplicates else "N/A"}
Email time: {self.email_time if self.jobs_no_duplicates else "N/A"}""")


s = Stats()
