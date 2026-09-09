# DS

**Pyrogram userbot for delay spam in multiple chats**

[![CI](https://github.com/kastaid/ds/workflows/CI/badge.svg)](https://github.com/kastaid/ds/actions/workflows/ci.yml)
[![LICENSE](https://img.shields.io/github/license/kastaid/ds)](LICENSE)
![Version](https://img.shields.io/github/manifest-json/v/kastaid/ds?label=Version)

> [!WARNING]
> Your Telegram account may get banned if this userbot is misused. We are not responsible for any spam, violations, or account restrictions.
>
> Use it at your own risk and review the [Telegram API Terms](https://core.telegram.org/api/terms).

## Table of Contents

- [Requirements](#requirements)
- [Quick Start](#quick-start)
  - [Clone Repository](#clone-repository)
    - [String Session](#string-session)
    - [Config](#config)
- [Deployments](#deployments)
  - [Docker Compose](#docker-compose)
  - [Locally](#locally)
- [Usage](#usage)
- [Update](#update)
- [Supports](#supports)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- Python 3.14+
- Linux (Debian/Ubuntu)
- Telegram `API_ID` and `API_HASH` from [API development tools](https://my.telegram.org)

## Quick Start

Follow these steps to set up and run **DS** on your system.

### Clone Repository

```sh
git clone https://github.com/kastaid/ds.git
cd ds
```

#### String Session

Generate `STRING_SESSION` by running `python3 strgen.py`, or directly:
```sh
python3 -c "import urllib.request as r;exec(r.urlopen('https://gist.githubusercontent.com/illvart/05a462d25ef1a99278201c5ee6b5ff14/raw').read())"
```
or using Docker:
```sh
docker run --rm -it python:3.14-alpine python3 -c "import urllib.request as r;exec(r.urlopen('https://gist.githubusercontent.com/illvart/05a462d25ef1a99278201c5ee6b5ff14/raw').read())"
```

#### Config

Create a `.env` file in the main directory and fill it with the example from [example.env](example.env).

## Deployments

Choose your preferred deployment method below.

### Docker Compose

Deploy using Docker Compose for easy containerized deployment.

```sh
git pull && \
  docker compose up -d --build && \
  docker compose logs -f
```

### Locally

Run DS locally on your machine or server (e.g., on Termux).

We recommend using [uv](https://docs.astral.sh/uv/) for faster and more reliable Python package management.

#### Production
Using uv:
```sh
uv pip install -r requirements.txt
python3 -m ds
```
Using pip:
```sh
pip3 install -r requirements.txt
python3 -m ds
```

#### Development
Using uv:
```sh
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt
python3 -m run --watch
```
Using pip:
```sh
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
python3 -m run --watch
```

More commands: run `python3 -m run -h`.

## Usage

Once successfully deployed, test your DS by sending `ping` in any chat.

### Start DS
Usage:
```sh
ds [delay] [count] [forward (reply only)] [text/reply] [to=chat]
ds1 [delay] [count] [forward (reply only)] [text/reply] [to=chat]
```
Examples:
```sh
ds 5 10 ok
ds1 9 5 cool
```
You can run up to 10 independent DS tasks (`ds` - `ds9`).

Send to a specific chat:
```sh
ds 5 10 ok to=@username
ds1 9 5 cool to=-1001234567890
```

Reply to a message and use `forward` to forward it instead of copying:
```sh
ds 5 10 forward
```

### Cancel
Cancel DS in a specific chat:
```sh
dscancel [to=chat]
ds1cancel [to=chat]
```

### Stop
Stop DS tasks in all chats:
```sh
dsstop
ds1stop
```

### Clear
Stop and clear all DS tasks:
```sh
dsclear
```

For more details, see [delayspam.py](ds/plugins/delayspam.py).

## Update

DS supports updating through Git.

For manual updates:
```sh
git pull
```
If you updated from an older version and experience errors, fix your local repo with:
```sh
git fetch origin && git reset --hard origin/main
```
This is **NOT** required for fresh installs.

## Supports

If you’re enjoying it or want to support development, feel free to donate. Thank you! ❤️

## Contributing

Want to contribute? Read the [Contributing](docs/CONTRIBUTING.md).

## License

Released under the [MIT License](LICENSE).
