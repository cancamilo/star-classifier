FROM python:3.10-slim AS python-base

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

FROM python-base AS builder-base
RUN buildDeps="build-essential" \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        gcc \
        libsasl2-dev \
        $buildDeps \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.4.2

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# Run time image
FROM python-base as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder-base ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app
COPY app ./
COPY models ./models

EXPOSE 8000
ENTRYPOINT ["hypercorn", "--bind", "0.0.0.0:8000", "predict_service:app"]