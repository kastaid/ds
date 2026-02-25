# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

FROM python:3.12-slim-trixie AS builder
ENV VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:/root/.local/bin:$PATH
WORKDIR /app
COPY requirements.txt /tmp/
RUN set -eux && \
    apt-get -qqy update && \
    apt-get -qqy install --no-install-recommends \
        build-essential curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    python -m venv $VIRTUAL_ENV && \
    uv pip install --python $VIRTUAL_ENV/bin/python -r /tmp/requirements.txt

FROM python:3.12-slim-trixie
ENV PATH=/opt/venv/bin:$PATH
WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY . .

CMD ["python", "-m", "ds"]
