FROM python:3.14.0-slim

WORKDIR /jobfitai

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "-u","main.py"]
