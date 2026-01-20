# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

FROM python:3.12-alpine AS builder

ENV VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH

WORKDIR /app
COPY requirements.txt /tmp/

RUN set -eux && \
    apk add --no-cache \
        build-base \
        libffi-dev \
        cargo && \
    python -m venv $VIRTUAL_ENV && \
    $VIRTUAL_ENV/bin/pip install --upgrade pip && \
    $VIRTUAL_ENV/bin/pip install --no-cache-dir --disable-pip-version-check --default-timeout=100 -r /tmp/requirements.txt

FROM python:3.12-alpine

ENV PATH=/opt/venv/bin:$PATH

WORKDIR /app

RUN set -eux && \
    apk add --no-cache \
        tini && \
    rm -rf -- /var/cache/apk/* /usr/share/man/* /usr/share/doc/* /tmp/* /var/tmp/*

COPY --from=builder /opt/venv /opt/venv
COPY . .

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["python", "-m", "ds"]
