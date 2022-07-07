
FROM python:3.9
COPY . /app
WORKDIR /app

ARG PG_DSN
ENV PG_DSN=$PG_DSN_ALC

RUN pip install --no-cache-dir -r /app/requirements.txt
ENTRYPOINT bash run.sh