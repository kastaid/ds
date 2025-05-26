FROM python:3.12-alpine

ENV TZ=Asia/Jakarta \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:/app/bin:$PATH

WORKDIR /app
COPY requirements.txt /tmp/

RUN set -eux && \
    apk add --no-cache \
        tini \
        musl-locales \
        tzdata \
        gcc \
        musl-dev \
        libffi-dev \
        openssl-dev \
        rust \
        cargo && \
	cp /usr/share/zoneinfo/${TZ} /etc/localtime && \
    echo "${TZ}" > /etc/timezone && \
    python -m venv $VIRTUAL_ENV && \
    $VIRTUAL_ENV/bin/pip install --upgrade pip && \
    $VIRTUAL_ENV/bin/pip install --no-cache-dir --disable-pip-version-check --default-timeout=100 -r /tmp/requirements.txt && \
    apk del \
        gcc \
        musl-dev \
        libffi-dev \
        openssl-dev \
        rust \
        cargo && \
    rm -rf /var/cache/apk/* /usr/share/man/* /usr/share/doc/* /tmp/* /var/tmp/*

COPY . .

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["python", "-m", "ds"]
