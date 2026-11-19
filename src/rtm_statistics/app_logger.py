"""Central logger: the only module that touches `logging` directly."""

import logging

from rtm_statistics.constants import APP_NAME, DEFAULT_LOG_LEVEL

_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


class AppLogger:
    """Thin wrapper so log level and output are configured in one place."""

    _logger = logging.getLogger(APP_NAME)

    @classmethod
    def configure(cls, level: str = DEFAULT_LOG_LEVEL) -> None:
        if not cls._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(_FORMAT))
            cls._logger.addHandler(handler)
        cls._logger.setLevel(level.upper())

    @classmethod
    def info(cls, message: str) -> None:
        cls._logger.info(message)

    @classmethod
    def warning(cls, message: str) -> None:
        cls._logger.warning(message)

    @classmethod
    def error(cls, message: str) -> None:
        cls._logger.error(message)
