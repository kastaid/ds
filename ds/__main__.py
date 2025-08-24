# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

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
    except (
        KeyboardInterrupt,
        SystemExit,
    ):
        pass
    except ImportError as err:
        LOG.exception(f"[MAIN_MODULE_IMPORT]: {err}")
        sys.exit(1)
    except Exception as err:
        LOG.exception(f"[MAIN_ERROR]: {err}")
    finally:
        LOG.warning("[MAIN] - Stopped...")
        sys.exit(0)
