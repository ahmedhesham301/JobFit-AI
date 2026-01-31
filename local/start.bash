#!/bin/bash

# git -C /JobFit-AI pull >> /var/log/job.log 2>&1

/JobFit-AI/local/myenv/bin/python -u /JobFit-AI/local/main.py || true

shutdown +1
