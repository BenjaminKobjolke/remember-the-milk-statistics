from pathlib import Path

import pytest

from rtm_statistics.config import ConfigError, load_settings, save_token
from tests.conftest import SMART_LIST_NAME, write_settings


def test_load_settings_reads_all_values(tmp_path: Path) -> None:
    ini = tmp_path / "settings.ini"
    write_settings(ini, tmp_path / "db.sqlite")

    settings = load_settings(ini)

    assert settings.api_key == "key"
    assert settings.token == "tok"
    assert settings.smart_list == SMART_LIST_NAME
    assert settings.completed_filter is None
    assert settings.database_path == tmp_path / "db.sqlite"
    assert settings.log_level == "INFO"


def test_load_settings_reads_completed_filter_override(tmp_path: Path) -> None:
    ini = tmp_path / "settings.ini"
    write_settings(ini, tmp_path / "db.sqlite")
    ini.write_text(
        ini.read_text(encoding="utf-8").replace("[output]", "completed_filter = list:Inbox\n[output]"),
        encoding="utf-8",
    )

    assert load_settings(ini).completed_filter == "list:Inbox"


def test_load_settings_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(ConfigError):
        load_settings(tmp_path / "nope.ini")


def test_load_settings_missing_required_value_raises(tmp_path: Path) -> None:
    ini = tmp_path / "settings.ini"
    ini.write_text("[rtm]\napi_key = key\n", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_settings(ini)


def test_save_token_keeps_other_values(tmp_path: Path) -> None:
    ini = tmp_path / "settings.ini"
    write_settings(ini, tmp_path / "db.sqlite", token="")

    save_token(ini, "new-token")

    settings = load_settings(ini)
    assert settings.token == "new-token"
    assert settings.smart_list == SMART_LIST_NAME
