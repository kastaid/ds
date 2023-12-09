# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

import asyncio
import sys
from pyrogram.raw.functions.account import DeleteAccount
from pyrogram.sync import idle
from . import LOOP
from .bot import User
from .logger import LOGS

DeleteAccount.__new__ = None


async def main() -> None:
    await User.start()
    await idle()
    await User.stop()


if __name__ == "__main__":
    try:
        LOOP.run_until_complete(main())
    except (
        ConnectionError,
        TimeoutError,
        asyncio.exceptions.CancelledError,
    ):
        pass
    except RuntimeError as err:
        LOGS.warning(f"[MAIN_WARNING] : {err}")
    except ImportError as err:
        LOGS.exception(f"[MAIN_MODULE_IMPORT] : {err}")
        sys.exit(1)
    except Exception as err:
        LOGS.exception(f"[MAIN_ERROR] : {err}")
    finally:
        LOGS.warning("[MAIN] - Stopped...")
        sys.exit(0)
