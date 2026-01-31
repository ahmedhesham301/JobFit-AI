#!/bin/bash

git -C /JobFit-AI pull >> /var/log/job.log 2>&1

/JobFit-AI/local/myenv/bin/python /JobFit-AI/local/main.py >> /var/log/job.log 2>&1 || true

# shutdown +1
shutdown -c
