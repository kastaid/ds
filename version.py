# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License


def get_version() -> str:
    import json

    with open("manifest.json") as f:
        data = json.load(f)
    return data.get("version", "unknown")


__version__ = get_version()
