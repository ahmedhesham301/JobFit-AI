import logging
class Stats:
    def __init__(self):
        self.scraping_time = None
        self.filter_time = None
        self.email_time = None

    def print(self):
        print(f"""Scraping time: {self.scraping_time}
Filter_time: {self.filter_time}
Email time: {self.email_time}""")
