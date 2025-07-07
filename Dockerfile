FROM python:3.12-alpine AS builder

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH

WORKDIR /app
COPY requirements.txt /tmp/

RUN set -eux && \
    apk add --no-cache \
        gcc \
        musl-dev \
        libffi-dev \
        openssl-dev \
        rust \
        cargo && \
    python -m venv $VIRTUAL_ENV && \
    $VIRTUAL_ENV/bin/pip install --upgrade pip && \
    $VIRTUAL_ENV/bin/pip install --no-cache-dir --disable-pip-version-check --default-timeout=100 -r /tmp/requirements.txt

FROM python:3.12-alpine

ENV TZ=Asia/Jakarta \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH

WORKDIR /app

RUN set -eux && \
    apk add --no-cache \
        tini \
        musl-locales \
        tzdata && \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime && \
    echo "${TZ}" > /etc/timezone && \
    rm -rf -- /var/cache/apk/* /usr/share/man/* /usr/share/doc/* /tmp/* /var/tmp/*

COPY --from=builder /opt/venv /opt/venv
COPY . .

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["python", "-m", "ds"]
