"""The snapshots table must match the shared contract (contract/ submodule)."""

import json
from pathlib import Path

import pytest

from rtm_statistics.constants import SNAPSHOTS_TABLE
from rtm_statistics.contract import CONTRACT_FILE, contract_columns
from rtm_statistics.storage import SnapshotColumn, SnapshotStore


def test_columns_reads_table_definition(tmp_path: Path) -> None:
    columns = SnapshotStore(tmp_path / "stats.sqlite").columns()

    assert SnapshotColumn("id", "INTEGER") in columns
    assert SnapshotColumn("taken_at", "TEXT") in columns


def test_snapshot_table_matches_contract(tmp_path: Path) -> None:
    if not CONTRACT_FILE.exists():
        pytest.skip("contract/ submodule not checked out")
    contract = json.loads(CONTRACT_FILE.read_text(encoding="utf-8"))

    actual = contract_columns(SnapshotStore(tmp_path / "stats.sqlite"))

    assert actual == contract[SNAPSHOTS_TABLE]["columns"], (
        "Table differs from contract/schema.json; follow the contract README change order, "
        "then run tools\\export_contract.bat"
    )
