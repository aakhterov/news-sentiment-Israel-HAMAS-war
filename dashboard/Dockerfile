FROM python:3.10-slim

MAINTAINER Alexander Akhterov "a.ahterov@gmail.com"

RUN apt-get update && apt-get install
WORKDIR /app/dashboard
COPY . /app/dashboard
COPY requirements.txt /app/dashboard
RUN pip install -r /app/dashboard/requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/app/dashboard"
EXPOSE 8050
CMD gunicorn -b 0.0.0.0:8050 --log-level=DEBUG 'app:server'