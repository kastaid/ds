# ruff: noqa
# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

import sys

try:
    import tgcrypto
except ImportError:
    try:
        import warpcrypto

        sys.modules["tgcrypto"] = warpcrypto
    except ImportError:
        pass


def _validate_tgcrypto() -> None:
    try:
        import tgcrypto
    except ImportError:
        raise RuntimeError("Missing crypto library. Install one of: pytgcrypto, TgCryptoRust, or WarpCrypto.") from None


_PINNED_VERSION = "2.2.25"


def _validate_version() -> None:
    from pyrogram import __version__

    if __version__ != _PINNED_VERSION:
        raise RuntimeError(
            f"Kurigram version mismatch: expected {_PINNED_VERSION}, found {__version__}. "
            "Review all upstream changes before updating the pinned version."
        )


def apply() -> None:
    _validate_version()
    _validate_tgcrypto()

    # Import order matters (dependency chain)
    from . import types
    from . import dispatcher
    from . import handlers
