"""Interactive RTM authorization (browser + polling), ported from remember-the-milk-exporter."""

import time
import webbrowser

from rtmilk import APIError, AuthorizationSession

from rtm_statistics.app_logger import AppLogger
from rtm_statistics.constants import AUTH_MAX_ATTEMPTS, AUTH_PERMS, AUTH_POLL_SECONDS


class AuthorizationTimeoutError(Exception):
    """The user did not authorize the app in time."""


def authorize(api_key: str, shared_secret: str) -> str:
    session = AuthorizationSession(api_key, shared_secret, AUTH_PERMS)
    AppLogger.info(f"Opening authorization URL in your browser: {session.url}")
    webbrowser.open(session.url)
    for attempt in range(1, AUTH_MAX_ATTEMPTS + 1):
        time.sleep(AUTH_POLL_SECONDS)
        try:
            token = str(session.Done())
        except APIError:
            AppLogger.info(f"Waiting for authorization... (attempt {attempt}/{AUTH_MAX_ATTEMPTS})")
            continue
        AppLogger.info("Authorization successful.")
        return token
    raise AuthorizationTimeoutError("Authorization timed out. Run sign_in.bat again.")
