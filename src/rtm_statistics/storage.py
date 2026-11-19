"""SQLite storage for snapshots; the future UI reads the same table."""

import sqlite3
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS snapshots (
    id INTEGER PRIMARY KEY,
    taken_at TEXT NOT NULL,
    list_name TEXT NOT NULL,
    open_count INTEGER NOT NULL,
    completed_count INTEGER NOT NULL
)
"""
_INSERT = "INSERT INTO snapshots (taken_at, list_name, open_count, completed_count) VALUES (?, ?, ?, ?)"
_SELECT_ALL = "SELECT taken_at, list_name, open_count, completed_count FROM snapshots ORDER BY id"
_TABLE_INFO = "PRAGMA table_info(snapshots)"


@dataclass(frozen=True)
class Snapshot:
    taken_at: datetime
    list_name: str
    open_count: int
    completed_count: int


@dataclass(frozen=True)
class SnapshotColumn:
    name: str
    type: str


class SnapshotStore:
    def __init__(self, path: Path) -> None:
        self._path = path

    def _connect(self) -> sqlite3.Connection:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self._path)
        connection.execute(_CREATE_TABLE)
        return connection

    def insert(self, snapshot: Snapshot) -> None:
        with closing(self._connect()) as connection, connection:
            connection.execute(
                _INSERT,
                (snapshot.taken_at.isoformat(), snapshot.list_name, snapshot.open_count, snapshot.completed_count),
            )

    def all(self) -> list[Snapshot]:
        with closing(self._connect()) as connection:
            rows = connection.execute(_SELECT_ALL).fetchall()
        return [Snapshot(datetime.fromisoformat(row[0]), row[1], row[2], row[3]) for row in rows]

    def columns(self) -> list[SnapshotColumn]:
        with closing(self._connect()) as connection:
            rows = connection.execute(_TABLE_INFO).fetchall()
        # PRAGMA table_info row: (cid, name, type, notnull, dflt_value, pk)
        return [SnapshotColumn(row[1], row[2]) for row in rows]
