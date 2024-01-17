FROM python:3.8.10

# Установка пакетов
WORKDIR /app

RUN apt-get update \
    && apt-get install -y netcat-openbsd
RUN pip install --upgrade pip \
    && pip install pipenv 

ARG PIPFILE
ARG PIPFILE_LOCK

COPY $PIPFILE $PIPFILE_LOCK /app/

RUN pipenv sync

CMD sh -c 'until nc -z -v -w30 mysql 3306; do echo "Waiting for MySQL to be ready..."; sleep 25; done' && pipenv run flask run