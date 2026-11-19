"""Shared test helpers: real rtmilk models, no network."""

from pathlib import Path
from unittest.mock import MagicMock

from rtmilk import RTMList, RTMSmartList
from rtmilk.client import Task, _Client

SMART_LIST_NAME = "Today"
SMART_FILTER = "status:incomplete AND dueBefore:today"
# What the tool must derive from SMART_FILTER for the "completed today" query
COMPLETED_FILTER = "(status:completed AND dueBefore:today) AND completed:today"


def make_task(completed: bool) -> Task:
    task = Task(None, "1", "2", "3")
    task.complete._LoadValue(completed)
    return task


def make_lists() -> list[RTMList]:
    common = {"deleted": False, "locked": False, "archived": False, "position": 0}
    return [
        RTMList(id="1", name="Inbox", smart=False, **common),
        RTMSmartList(id="2", name=SMART_LIST_NAME, smart=True, filter=SMART_FILTER, **common),
    ]


def make_client(results: dict[str, list[Task]] | None = None) -> MagicMock:
    """Fake RTM client: GetLists returns make_lists(), Get(filter) returns results[filter]."""
    client = MagicMock(spec=_Client)
    client.GetLists.return_value = make_lists()
    client.Get.side_effect = lambda f: (results or {})[f]
    return client


def write_settings(path: Path, database: Path, token: str = "tok") -> None:
    path.write_text(
        "[rtm]\n"
        "api_key = key\n"
        "shared_secret = secret\n"
        f"token = {token}\n"
        "[tracking]\n"
        f"smart_list = {SMART_LIST_NAME}\n"
        "[output]\n"
        f"database = {database}\n",
        encoding="utf-8",
    )
