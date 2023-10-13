FROM python:3.10-slim-bullseye

ENV TZ=Asia/Jakarta \
    TERM=xterm-256color \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    VIRTUAL_ENV=/venv \
    PATH=/venv/bin:/app/bin:$PATH

WORKDIR /app
COPY . .

RUN set -ex \
    && apt-get -qqy update \
    && apt-get -qqy install --no-install-recommends \
        tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && dpkg-reconfigure --force -f noninteractive tzdata >/dev/null 2>&1 \
    && python3 -m venv $VIRTUAL_ENV \
    && pip3 install --disable-pip-version-check --default-timeout=100 --no-cache-dir -r requirements.txt \
    && apt-get -qqy clean \
    && rm -rf -- ~/.cache /var/lib/apt/lists/* /var/cache/apt/archives/* /etc/apt/sources.list.d/* /usr/share/man/* /usr/share/doc/* /var/log/* /tmp/* /var/tmp/*

CMD ["python3", "-m", "ds"]
