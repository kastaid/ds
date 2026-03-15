# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

import sys

import uvloop
from pyrogram.sync import compose

from .kasta import KastaClient
from .logger import LOG
from .patcher import *  # noqa


async def main() -> None:
    await compose([KastaClient()])


if __name__ == "__main__":
    try:
        uvloop.run(main())
    except KeyboardInterrupt:
        LOG.warning("[APP] Shutdown signal received.")
    except Exception as err:
        LOG.exception(f"[APP] Unhandled exception: {err}")
        sys.exit(1)
    finally:
        LOG.warning("[APP] Stopped.")
