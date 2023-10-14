FROM python:3.10.6-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /usr/src/app

RUN apt-get update \
    && apt-get install -y netcat libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade --no-cache-dir pip \
    && pip install --no-cache-dir poetry==1.2.2

COPY ./pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-interaction --no-ansi

COPY ./ ./
COPY ./entrypoint.sh ./
RUN chmod 777 /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
