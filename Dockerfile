FROM python:3.12.0-alpine

VOLUME [ "/config" ]

RUN mkdir /app && \
    pip install porkbun-ddns==1.1.2 apscheduler==3.10.4

WORKDIR /app
COPY ./entrypoint.py /app

ENTRYPOINT [ "python", "entrypoint.py" ]