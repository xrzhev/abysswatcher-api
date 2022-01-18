FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-alpine3.14-2021-10-02
COPY ./src /app
COPY ./requirements.txt /tmp
WORKDIR /app
ENV SLACK_WEBHOOK_URL=""
RUN set -x && \
    apk --update add tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del tzdata && \
    rm -rf /var/cache/apk/* && \ 
    pip3 install -r /tmp/requirements.txt && \
    python3 /app/migrate_db.py
