FROM python:3.12.0-alpine

VOLUME [ "/config" ]

RUN mkdir /app && \
    pip install porkbun-ddns apscheduler

WORKDIR /app
COPY ./entrypoint.py /app

ENTRYPOINT [ "python", "entrypoint.py" ]