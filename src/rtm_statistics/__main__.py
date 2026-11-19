"""Entry point: `python -m rtm_statistics [--auth-only]`."""

import sys
from pathlib import Path

from rtm_statistics.app import run
from rtm_statistics.app_logger import AppLogger
from rtm_statistics.constants import AUTH_ONLY_FLAG, DEFAULT_SETTINGS_FILE


def main() -> None:
    AppLogger.configure()
    sys.exit(run(Path(DEFAULT_SETTINGS_FILE), auth_only=AUTH_ONLY_FLAG in sys.argv))


if __name__ == "__main__":
    main()
