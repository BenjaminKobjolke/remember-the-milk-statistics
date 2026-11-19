"""Orchestrates one run and is the central error handler."""

from datetime import UTC, datetime
from pathlib import Path

from rtmilk import APIError, CreateClient

from rtm_statistics.app_logger import AppLogger
from rtm_statistics.auth import AuthorizationTimeoutError, authorize
from rtm_statistics.config import ConfigError, Settings, load_settings, save_token
from rtm_statistics.constants import EXIT_ERROR, EXIT_OK, INVALID_TOKEN_CODE
from rtm_statistics.rtm_source import SmartListNotFoundError, take_snapshot
from rtm_statistics.storage import Snapshot, SnapshotStore


def _sign_in(settings_path: Path, settings: Settings) -> str:
    token = authorize(settings.api_key, settings.shared_secret)
    save_token(settings_path, token)
    AppLogger.info(f"Token saved to {settings_path}")
    return token


def _snapshot(settings: Settings, token: str) -> Snapshot:
    client = CreateClient(settings.api_key, settings.shared_secret, token)
    return take_snapshot(client, settings.smart_list, settings.completed_filter, datetime.now(UTC))


def _snapshot_with_reauth(settings_path: Path, settings: Settings) -> Snapshot:
    token = settings.token or _sign_in(settings_path, settings)
    try:
        return _snapshot(settings, token)
    except APIError as error:
        if error.code != INVALID_TOKEN_CODE:
            raise
        AppLogger.warning("Auth token is invalid. Re-authorizing once...")
        return _snapshot(settings, _sign_in(settings_path, settings))


def run(settings_path: Path, auth_only: bool) -> int:
    try:
        settings = load_settings(settings_path)
        AppLogger.configure(settings.log_level)
        if auth_only:
            _sign_in(settings_path, settings)
            return EXIT_OK
        snapshot = _snapshot_with_reauth(settings_path, settings)
        SnapshotStore(settings.database_path).insert(snapshot)
    except (ConfigError, SmartListNotFoundError, AuthorizationTimeoutError) as error:
        AppLogger.error(str(error))
        return EXIT_ERROR
    except APIError as error:
        AppLogger.error(f"RTM API error (code {error.code}): {error.message}")
        return EXIT_ERROR
    AppLogger.info(f"Snapshot '{snapshot.list_name}': open={snapshot.open_count} completed={snapshot.completed_count}")
    return EXIT_OK
