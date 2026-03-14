# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

import json

from . import Root

EXCLUDE = (".mypy_cache", "db")


def main() -> None:
    for p in filter(lambda x: not str(x.parent).endswith(EXCLUDE), Root.rglob("*.json")):
        try:
            with p.open(encoding="utf-8") as f:
                data = json.load(f)
            with p.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, sort_keys=False, ensure_ascii=False)
                print("Pretty print:", p.name)
        except Exception as err:
            print("Failed to pretty print:", str(err))


if __name__ == "__main__":
    raise SystemExit(main())
