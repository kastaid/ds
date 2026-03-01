# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

FROM python:3.12-slim-bookworm
ENV TERM=xterm \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:/root/.local/bin:$PATH
ARG UV_VERSION=0.10.7
WORKDIR /app
COPY requirements.txt .
RUN set -eux && \
    apt-get -qqy update && \
    apt-get -qqy install --no-install-recommends \
        build-essential curl && \
    curl -LsSf https://github.com/astral-sh/uv/releases/download/${UV_VERSION}/uv-installer.sh | sh && \
    python -m venv $VIRTUAL_ENV && \
    uv pip install --python $VIRTUAL_ENV/bin/python -r requirements.txt && \
    apt-get -qqy purge \
        curl && \
    apt-get -qqy autoremove && \
    apt-get clean

COPY . .

CMD ["python", "-m", "ds"]
