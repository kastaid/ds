# ruff: noqa E402
# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

import asyncio
import sys
import uvloop
from .patches import apply

apply()
from .kasta import KastaClient
from .logger import LOG

if __name__ == "__main__":
    try:
        asyncio.run(
            KastaClient().bootstrap(),
            loop_factory=uvloop.new_event_loop,
        )
    except KeyboardInterrupt:
        LOG.info("[APP] shutdown signal received")
    except Exception:
        LOG.exception("[APP] unhandled exception")
        sys.exit(1)
    finally:
        LOG.info("[APP] stopped")
