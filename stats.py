class Stats:
    def __init__(self):
        self.scraping_time = None
        self.filter_time = None
        self.email_time = None
        self.jobs_no_duplicates = 0
        self.jobs_duplicates = 0

    def print(self):
        print(
            f"""Total jobs with duplicates: {self.jobs_duplicates}
Total jobs no duplicates: {self.jobs_no_duplicates}
Scraping time: {self.scraping_time}
Filter_time: {self.filter_time}
AVG request time: {self.filter_time / self.jobs_no_duplicates}
Email time: {self.email_time}"""
        )
