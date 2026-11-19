from datetime import UTC, datetime
from pathlib import Path

from rtm_statistics.storage import Snapshot, SnapshotStore


def test_insert_creates_table_and_reads_back(tmp_path: Path) -> None:
    db = tmp_path / "sub" / "stats.sqlite"
    store = SnapshotStore(db)
    first = Snapshot(datetime(2026, 11, 19, 8, 0, tzinfo=UTC), "Today", 12, 0)
    second = Snapshot(datetime(2026, 11, 19, 9, 0, tzinfo=UTC), "Today", 10, 3)

    store.insert(first)
    store.insert(second)

    assert db.exists()
    assert SnapshotStore(db).all() == [first, second]
