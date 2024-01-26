# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

import sys
import uvloop
from pyrogram.sync import idle
from ds.logger import LOG
from ds.patcher import *  # noqa
from ds.user import UserClient


async def main() -> None:
    await UserClient().start()
    await idle()
    await UserClient().stop()


if __name__ == "__main__":
    try:
        uvloop.run(main())
    except (
        KeyboardInterrupt,
        SystemExit,
        TimeoutError,
    ):
        pass
    except ImportError as err:
        LOG.exception(f"[MAIN_MODULE_IMPORT] : {err}")
        sys.exit(1)
    except Exception as err:
        LOG.exception(f"[MAIN_ERROR] : {err}")
    finally:
        LOG.warning("[MAIN] - Stopped...")
        sys.exit(0)
