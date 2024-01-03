FROM python:3.10-slim

MAINTAINER Alexander Akhterov "a.ahterov@gmail.com"

RUN apt-get update && apt-get install -y cron && which cron && \
    rm -rf /etc/cron.*/*

WORKDIR /app
COPY . /app/news_collector
RUN pip install -r /app/news_collector/requirements.txt

COPY crontab /etc

ENV PYTHONPATH="/app"

ENTRYPOINT ["/app/news_collector/entrypoint.sh"]