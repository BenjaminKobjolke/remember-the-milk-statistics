# Remember The Milk Statistics

Tracks how the number of todos on a Remember The Milk **smart list** goes up and down over
the day. Every run takes one snapshot and appends it to a SQLite file:

- **open count** — incomplete tasks returned by the smart list's filter (read from RTM on
  every run, so edits to the smart list apply automatically)
- **completed count** — tasks completed today that belong to the smart list. The query is
  derived from the smart list's filter: `status:incomplete` is replaced by `status:completed`
  and ` AND completed:today` is appended, so finished overdue and undated tasks count too.
  Set the optional `completed_filter` in `settings.ini` to use your own RTM search instead.

A UI to display the data can read the database later.

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Git (the `rtmilk` dependency is installed from GitHub)
- An RTM API key and shared secret: https://www.rememberthemilk.com/services/api/keys.rtm

## Setup

1. `install.bat` — creates the virtual environment and runs the tests.
2. Copy `settings_example.ini` to `settings.ini` and fill in `api_key`, `shared_secret` and
   `smart_list`.
3. `sign_in.bat` — opens the RTM authorization page in the browser and stores the token in
   `settings.ini`.

## Usage

```bat
start.bat
```

Takes one snapshot and exits (exit code 0 on success, 1 on error). To track the day,
schedule `start.bat` in **Windows Task Scheduler**, e.g. every 15 minutes.

If the token becomes invalid, the next run opens the authorization page once and retries.

### Inspect the data

```bat
uv run python -c "import sqlite3; print(sqlite3.connect('data/statistics.sqlite').execute('select * from snapshots').fetchall())"
```

## Database

`[output] database` (default `data/statistics.sqlite`):

```sql
CREATE TABLE snapshots (
    id INTEGER PRIMARY KEY,
    taken_at TEXT NOT NULL,          -- ISO 8601, UTC
    list_name TEXT NOT NULL,         -- smart list name
    open_count INTEGER NOT NULL,
    completed_count INTEGER NOT NULL
);
```

### Schema contract

The table is shared with
[remember-the-milk-statistics-frontend](../remember-the-milk-statistics-frontend) through the
[remember-the-milk-statistics-contract](https://github.com/BenjaminKobjolke/remember-the-milk-statistics-contract)
submodule at `contract/`. Clone with `--recurse-submodules`, or run
`git submodule update --init contract`.

- `tests/unit/test_contract.py` fails when the table no longer matches `contract/schema.json`.
- After a deliberate schema change, run `tools\export_contract.bat`, then commit and push the
  contract repo first. Follow the change order in the contract README: a dropped or renamed
  column breaks the frontend.

## Development

| Script | Purpose |
| --- | --- |
| `tools\run_tests.bat` | unit tests (`tests/unit`) |
| `tools\run_integration_tests.bat` | integration tests (`tests/integration`, no live API) |
| `update.bat` | upgrade dependencies, lint, type check, test |
| `tools\graphify_update.bat` | refresh the graphify code graph of `src/` |
| `tools\export_contract.bat` | write the table definition into `contract/schema.json` |

Checks: `uv run ruff check src tests`, `uv run ruff format --check src tests`, `uv run mypy src`.
