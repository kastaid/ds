# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

FROM python:3.14-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.10.11 /uv /uvx /bin/
ENV TERM=xterm \
    PATH=/opt/venv/bin:$PATH \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1
WORKDIR /app
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv /opt/venv && \
    uv pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "ds"]
