# ds - delayspam
> Pyrogram **userbot** for delay spam a message with multi chats.

<p align="center">
    <img alt="Version" src="https://img.shields.io/github/manifest-json/v/kastaid/ds" />
    <a href="https://github.com/kastaid/ds/blob/main/LICENSE"><img alt="LICENSE" src="https://img.shields.io/github/license/kastaid/ds" /></a>
    <a href="https://telegram.me/kastaid"><img alt="Telegram" src="https://img.shields.io/badge/kastaid-blue?logo=telegram" /></a>
</p>

## clone this repo
```sh
git clone https://github.com/kastaid/ds \
  && cd ds
```

## create config file
`nano -c config.env`
```sh
API_ID=
API_HASH=
STRING_SESSION=
HANDLER=
```

## docker compose
```sh
git pull \
  && docker system prune -f \
  && docker compose up --detach --build --remove-orphans --no-color \
  && docker compose logs -f
```

## commands
Please read how to at [delayspam.py](https://github.com/kastaid/ds/blob/main/ds/plugins/delayspam.py).
```sh
ds 5 10 ok
dscancel
dsstop
dsclear
```
