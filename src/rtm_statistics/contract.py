"""Export the snapshots table definition into the shared contract (contract/schema.json).

Run via tools/export_contract.bat after a deliberate schema change. Production code never
reads the contract; tests compare against it.
"""

import json
import tempfile
from pathlib import Path

from rtm_statistics.app_logger import AppLogger
from rtm_statistics.constants import (
    CONTRACT_COLUMNS_KEY,
    CONTRACT_DIR,
    CONTRACT_SCHEMA_FILE,
    SNAPSHOTS_TABLE,
)
from rtm_statistics.storage import SnapshotStore

# Repo root is two levels above this package (src/rtm_statistics/)
CONTRACT_FILE = Path(__file__).resolve().parents[2] / CONTRACT_DIR / CONTRACT_SCHEMA_FILE


def contract_columns(store: SnapshotStore) -> dict[str, str]:
    """Columns in the contract's shape: name to SQLite type, sorted by name."""
    return {column.name: column.type for column in sorted(store.columns(), key=lambda c: c.name)}


def export() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        columns = contract_columns(SnapshotStore(Path(tmp) / "schema.sqlite"))
    schema = json.loads(CONTRACT_FILE.read_text(encoding="utf-8"))
    schema[SNAPSHOTS_TABLE][CONTRACT_COLUMNS_KEY] = columns
    # LF keeps the export byte-identical to the committed file on Windows
    CONTRACT_FILE.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8", newline="\n")
    AppLogger.info(f"Exported {len(columns)} {SNAPSHOTS_TABLE} columns to {CONTRACT_FILE}")


if __name__ == "__main__":
    AppLogger.configure()
    export()
