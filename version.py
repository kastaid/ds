# Copyright (C) 2023-present kastaid
# This file is part of https://github.com/kastaid/ds
# Please read the MIT License at
# https://github.com/kastaid/ds/blob/main/LICENSE


def get_version() -> str:
    import json

    with open("manifest.json") as f:
        data = json.load(f)
    return data.get("version", "unknown")


__version__ = get_version()
