class Status:
    def __init__(self):
        self.total_jobs = 0
        self.blacklisted_jobs = 0

    def print(self):
        print(f"""blacklisted jobs: {self.blacklisted_jobs}""")
