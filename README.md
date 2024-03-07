# ds - delayspam
> Pyrogram **userbot** for delay spam a message with multi chats.

<p align="center">
    <a href="https://github.com/kastaid/ds/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/kastaid/ds/ci.yml?branch=main&logo=github&label=CI" /></a>
    <img alt="Python" src="https://img.shields.io/badge/Python-3.11.x%20%7C%203.12.x-blue?logoColor=white&logo=python" />
    <img alt="Version" src="https://img.shields.io/github/manifest-json/v/kastaid/ds" />
    <a href="https://github.com/kastaid/ds/blob/main/LICENSE"><img alt="LICENSE" src="https://img.shields.io/github/license/kastaid/ds" /></a>
    <a href="https://telegram.me/kastaid"><img alt="Telegram" src="https://img.shields.io/badge/kastaid-blue?logo=telegram" /></a>
</p>

## Clone this repo
```sh
git clone https://github.com/kastaid/ds \
  && cd ds
```

## Create config file
`nano -c config.env`
```sh
API_ID=
API_HASH=
STRING_SESSION=
HANDLER=
```
Generate STRING_SESSION at https://t.me/strgen_bot (pyrofork).

## Docker Compose
```sh
git pull \
  && docker system prune -f \
  && docker compose up --detach --build \
  && docker compose logs -f
```

## Commands
Please read how to at [delayspam.py](https://github.com/kastaid/ds/blob/main/ds/plugins/delayspam.py).
```sh
ds 5 10 ok
ds1 9 5 cool

dscancel
ds1cancel

dsstop
ds1stop

dsclear
```
