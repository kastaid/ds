# ds

**Pyrogram userbot for delay spam in multiple chats**

[![CI](https://github.com/kastaid/ds/workflows/CI/badge.svg)](https://github.com/kastaid/ds/actions/workflows/ci.yml)
[![LICENSE](https://img.shields.io/github/license/kastaid/ds)](LICENSE)
![Version](https://img.shields.io/github/manifest-json/v/kastaid/ds?label=Version)

## Disclaimer

⚠️ **Important:** Your Telegram account may get banned. We are not responsible for any misuse of this userbot.

If you spam, face issues with Telegram, or get your account deleted, **DON’T BLAME US!**
- No personal support.
- We won’t spoon-feed you.
- If you need help, ask in our support group, and we or others will try to help you.
- **DWYOR** (Do With Your Own Risk).

Review the [Telegram API Terms of Service](https://core.telegram.org/api/terms).

Thank you for trusting and using this userbot!

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
- [Supports](#supports)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- Python 3.11.x
- Linux (recommended: Debian/Ubuntu)
- Telegram `API_ID` and `API_HASH` from [API development tools](https://my.telegram.org)

## Quick Start

Follow these steps to set up and run **ds** on your system.

### Clone Repository

```sh
git clone https://github.com/kastaid/ds.git
cd ds
```

#### String Session

Generate `STRING_SESSION` by choosing **Pyrofork** at [@strgen_bot](https://t.me/strgen_bot).

#### Config

Create a `.env` file in the main directory and fill it with the example from [example.env](example.env).

## Deployments

Choose your preferred deployment method below.

### Docker Compose

Deploy using Docker Compose for easy containerized deployment.

```sh
git pull && \
  docker compose up --detach --build --force-recreate && \
  docker compose logs -f
```

### Locally

Run ds locally on your machine or server (e.g., on Termux).

#### Production
```sh
pip3 install -r requirements.txt
python3 -m ds
```

#### Development
```sh
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
python3 -m run --watch
```

More commands: run `python3 -m run -h`.

## Usage

Once successfully deployed, test your ds by sending `ping` in any chat.

```sh
ds 5 10 ok
ds1 9 5 cool

dscancel
ds1cancel

dsstop
ds1stop

dsclear
```

Please read how the delay spam commands work at [delayspam.py](ds/plugins/delayspam.py).

## Supports

If you’re enjoying it or want to support development, feel free to donate. Thank you! ❤️

## Contributing

Want to contribute? Read the [Contributing](docs/CONTRIBUTING.md).

## License

Released under the [MIT License](LICENSE).
