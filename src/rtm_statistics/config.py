"""Loads settings.ini into a typed Settings object and persists the RTM token."""

import configparser
from dataclasses import dataclass
from pathlib import Path

from rtm_statistics.constants import (
    DEFAULT_DATABASE,
    DEFAULT_LOG_LEVEL,
    KEY_API_KEY,
    KEY_COMPLETED_FILTER,
    KEY_DATABASE,
    KEY_LOG_LEVEL,
    KEY_SHARED_SECRET,
    KEY_SMART_LIST,
    KEY_TOKEN,
    SECTION_LOGGING,
    SECTION_OUTPUT,
    SECTION_RTM,
    SECTION_TRACKING,
)


class ConfigError(Exception):
    """settings.ini is missing or incomplete."""


@dataclass(frozen=True)
class Settings:
    api_key: str
    shared_secret: str
    token: str
    smart_list: str
    # None = derive the completed query from the smart list filter
    completed_filter: str | None
    database_path: Path
    log_level: str


def _read(path: Path) -> configparser.ConfigParser:
    if not path.is_file():
        raise ConfigError(f"Settings file not found: {path} (copy settings_example.ini)")
    # interpolation off: RTM filters may contain '%'
    parser = configparser.ConfigParser(interpolation=None)
    parser.read(path, encoding="utf-8")
    return parser


def _required(parser: configparser.ConfigParser, section: str, key: str) -> str:
    value = parser.get(section, key, fallback="").strip()
    if not value:
        raise ConfigError(f"Missing [{section}] {key} in settings.ini")
    return value


def load_settings(path: Path) -> Settings:
    parser = _read(path)
    return Settings(
        api_key=_required(parser, SECTION_RTM, KEY_API_KEY),
        shared_secret=_required(parser, SECTION_RTM, KEY_SHARED_SECRET),
        token=parser.get(SECTION_RTM, KEY_TOKEN, fallback="").strip(),
        smart_list=_required(parser, SECTION_TRACKING, KEY_SMART_LIST),
        completed_filter=parser.get(SECTION_TRACKING, KEY_COMPLETED_FILTER, fallback="").strip() or None,
        database_path=Path(parser.get(SECTION_OUTPUT, KEY_DATABASE, fallback=DEFAULT_DATABASE)),
        log_level=parser.get(SECTION_LOGGING, KEY_LOG_LEVEL, fallback=DEFAULT_LOG_LEVEL),
    )


def save_token(path: Path, token: str) -> None:
    # shortcut: configparser rewrite drops comments in settings.ini; fine for a local file
    parser = _read(path)
    parser.set(SECTION_RTM, KEY_TOKEN, token)
    with path.open("w", encoding="utf-8") as handle:
        parser.write(handle)
