FROM python:3.12-slim

WORKDIR /jobfitai

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN patchright install-deps

RUN patchright install

COPY . .

CMD [ "python3", "-u","main.py"]
