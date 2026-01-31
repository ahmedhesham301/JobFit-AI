#!/bin/bash

# git -C /JobFit-AI pull >> /var/log/job.log 2>&1

sleep 30

/JobFit-AI/local/myenv/bin/python -u /JobFit-AI/local/main.py >> /var/log/job.log 2>&1 || true


# shutdown +1
