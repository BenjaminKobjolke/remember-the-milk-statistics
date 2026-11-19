"""End-to-end run: settings file -> fake RTM client -> real SQLite file."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from rtmilk import APIError
from rtmilk.client import _Client

from rtm_statistics.app import run
from rtm_statistics.constants import INVALID_TOKEN_CODE
from rtm_statistics.storage import SnapshotStore
from tests.conftest import (
    COMPLETED_FILTER,
    SMART_FILTER,
    SMART_LIST_NAME,
    make_client,
    make_lists,
    make_task,
    write_settings,
)

pytestmark = pytest.mark.integration


def _fake_client() -> MagicMock:
    return make_client({SMART_FILTER: [make_task(False)], COMPLETED_FILTER: [make_task(True), make_task(True)]})


def test_run_appends_snapshot_each_time(tmp_path: Path) -> None:
    ini, db = tmp_path / "settings.ini", tmp_path / "data" / "stats.sqlite"
    write_settings(ini, db)

    with patch("rtm_statistics.app.CreateClient", return_value=_fake_client()):
        assert run(ini, auth_only=False) == 0
        assert run(ini, auth_only=False) == 0

    rows = SnapshotStore(db).all()
    assert [(r.list_name, r.open_count, r.completed_count) for r in rows] == [(SMART_LIST_NAME, 1, 2)] * 2


def test_run_reauthorizes_once_on_invalid_token(tmp_path: Path) -> None:
    ini, db = tmp_path / "settings.ini", tmp_path / "stats.sqlite"
    write_settings(ini, db, token="expired")
    broken = MagicMock(spec=_Client)
    broken.GetLists.side_effect = APIError(INVALID_TOKEN_CODE, "Invalid auth token")

    with (
        patch("rtm_statistics.app.CreateClient", side_effect=[broken, _fake_client()]),
        patch("rtm_statistics.app.authorize", return_value="fresh") as authorize,
    ):
        assert run(ini, auth_only=False) == 0

    authorize.assert_called_once()
    assert "token = fresh" in ini.read_text(encoding="utf-8")
    assert len(SnapshotStore(db).all()) == 1


def test_run_fails_for_unknown_smart_list(tmp_path: Path) -> None:
    ini, db = tmp_path / "settings.ini", tmp_path / "stats.sqlite"
    write_settings(ini, db)
    client = _fake_client()
    client.GetLists.return_value = make_lists()[:1]

    with patch("rtm_statistics.app.CreateClient", return_value=client):
        assert run(ini, auth_only=False) == 1

    assert not db.exists()
