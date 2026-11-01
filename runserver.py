#!/usr/bin/env python
"""Start the Minerva Django API wrapper from the project root."""

import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))


def configure_api_key(arguments):
    """Read the wrapper key before Django initializes its middleware."""
    if "--help" in arguments or "-h" in arguments:
        return arguments

    remaining = []
    api_key = None
    index = 0

    while index < len(arguments):
        argument = arguments[index]
        if argument == "--api-key":
            if index + 1 >= len(arguments):
                raise SystemExit("--api-key requires a value")
            api_key = arguments[index + 1]
            index += 2
            continue
        if argument.startswith("--api-key="):
            api_key = argument.split("=", 1)[1]
            index += 1
            continue
        remaining.append(argument)
        index += 1

    if api_key is None:
        raise SystemExit(
            "Missing API key. Start with: python runserver.py --api-key YOUR_KEY"
        )

    from minerva import configure_api_wrapper

    configure_api_wrapper(api_key)
    return remaining


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "minerva.ZermeloApiWrapper.settings",
)

from django.core.management import execute_from_command_line


if __name__ == "__main__":
    django_arguments = configure_api_key(sys.argv[1:])
    execute_from_command_line([sys.argv[0], "runserver", *django_arguments])
