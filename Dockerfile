# python-base with shared environment variables
FROM python:3.13-slim-bullseye AS python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1
ENV PATH="$POETRY_HOME/bin:$PATH"


# builder-base installs poetry
FROM python-base AS builder-base
RUN buildDeps="build-essential" \
    && apt-get update \
    && apt-get install --no-install-recommends -y curl \
    && apt-get install -y --no-install-recommends $buildDeps \
    && rm -rf /var/lib/apt/lists/*
ENV POETRY_VERSION=2.0.1
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 - --version ${POETRY_VERSION} && \
    chmod a+x /opt/poetry/bin/poetry


# 'development' stage installs all dev deps and can be used to develop code.
FROM python-base AS development
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
WORKDIR /app
COPY . .
RUN poetry install
ENV HOST="0.0.0.0"
ENV HOT_RELOAD=True
EXPOSE 8080
CMD ["poetry", "run", "python", "-m", "datamole_assignment.main"]
