FROM python:alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN apk update && \
    apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev && \
    apk add --no-cache postgresql-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apk del --no-cache .build-deps && \
    rm -rf /var/cache/apk/*
