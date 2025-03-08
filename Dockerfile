FROM python:3.12.0-alpine

VOLUME [ "/config" ]

ENV CONFIG_PATH=/config/config.json

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app
COPY ./entrypoint.py /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "entrypoint.py" ]
