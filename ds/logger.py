# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

import logging
import sys
from datetime import date
from loguru import logger as LOGS
from . import PROJECT

LOGS.remove(0)
LOGS.add(
    "logs/{}-{}.log".format(
        PROJECT,
        date.today().strftime("%Y-%m-%d"),
    ),
    format="{time:YY/MM/DD HH:mm:ss} | {level: <8} | {name: ^15} | {function: ^15} | {line: >3} : {message}",
    rotation="1 MB",
)
LOGS.add(
    sys.stderr,
    format="{time:YY/MM/DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    level="INFO",
    colorize=False,
)
LOGS.opt(lazy=True, colors=False)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = LOGS.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        LOGS.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


logging.disable(logging.DEBUG)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pyrogram.dispatcher").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.basicConfig(handlers=[InterceptHandler()], level="INFO")
