FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-alpine3.14-2021-10-02
COPY ./src /app
COPY ./requirements.txt /tmp
WORKDIR /tmp
RUN pip3 install -r ./requirements.txt
WORKDIR /app
