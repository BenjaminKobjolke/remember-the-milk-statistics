"""Reads the counts for one snapshot from Remember The Milk."""

from datetime import datetime

from rtmilk import RTMSmartList
from rtmilk.client import _Client

from rtm_statistics.constants import COMPLETED_TODAY_SUFFIX, STATUS_COMPLETED, STATUS_INCOMPLETE
from rtm_statistics.storage import Snapshot


class SmartListNotFoundError(Exception):
    """No smart list with the configured name exists."""


def find_smart_list_filter(client: _Client, name: str) -> str:
    for rtm_list in client.GetLists():
        if isinstance(rtm_list, RTMSmartList) and rtm_list.name == name:
            return str(rtm_list.filter)
    raise SmartListNotFoundError(f"No smart list named '{name}' found in RTM")


def completed_today_filter(smart_filter: str) -> str:
    """Same lists/conditions as the smart list, but for tasks finished today.

    Without the status swap, finished overdue/undated tasks would never match the smart list filter.
    """
    # shortcut: plain string replace; assumes the smart list uses status:incomplete literally,
    # upgrade to a parser if RTM filter syntax requires structural matching
    swapped = smart_filter.replace(STATUS_INCOMPLETE, STATUS_COMPLETED)
    return f"({swapped}) {COMPLETED_TODAY_SUFFIX}"


def take_snapshot(client: _Client, smart_list: str, completed_filter: str | None, now: datetime) -> Snapshot:
    smart_filter = find_smart_list_filter(client, smart_list)
    # The smart list's filter may also return completed tasks (e.g. dueWithin), so count incomplete only.
    tasks = client.Get(smart_filter)
    open_count = sum(1 for task in tasks if not task.complete.value)
    completed_count = len(client.Get(completed_filter or completed_today_filter(smart_filter)))
    return Snapshot(now, smart_list, open_count, completed_count)
