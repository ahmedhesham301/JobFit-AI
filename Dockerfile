FROM python:3.12.3-slim

WORKDIR /jobfitai

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN cp -rf .venv/lib/python3.12/site-packages/jobspy/* /usr/local/lib/python3.12/site-packages/jobspy/ && rm -rf .venv

CMD [ "python3", "-u","main.py"]
