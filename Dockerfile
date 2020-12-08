FROM python:3.7
WORKDIR /app

LABEL maintainer="manuel@e-bot7.com"
LABEL vendor="e-bot7"

COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT /app/src/entrypoint.sh