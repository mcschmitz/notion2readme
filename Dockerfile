FROM python:3.7

LABEL maintainer="manuel@e-bot7.com"
LABEL vendor="e-bot7"

COPY ./src src
COPY requirements.txt requirements.txt

RUN chmod +x src/entrypoint.sh
ENTRYPOINT src/entrypoint.sh