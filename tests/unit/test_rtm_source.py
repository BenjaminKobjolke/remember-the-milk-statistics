from datetime import UTC, datetime

import pytest

from rtm_statistics.rtm_source import (
    SmartListNotFoundError,
    completed_today_filter,
    find_smart_list_filter,
    take_snapshot,
)
from tests.conftest import COMPLETED_FILTER, SMART_FILTER, SMART_LIST_NAME, make_client, make_task


def test_find_smart_list_filter_by_name() -> None:
    assert find_smart_list_filter(make_client(), SMART_LIST_NAME) == SMART_FILTER


@pytest.mark.parametrize("name", ["Missing", "Inbox"])
def test_find_smart_list_filter_rejects_unknown_or_plain_list(name: str) -> None:
    with pytest.raises(SmartListNotFoundError):
        find_smart_list_filter(make_client(), name)


def test_take_snapshot_counts_open_and_completed() -> None:
    client = make_client(
        {
            SMART_FILTER: [make_task(False), make_task(True), make_task(False)],
            COMPLETED_FILTER: [make_task(True), make_task(True)],
        }
    )
    now = datetime(2026, 11, 19, 8, 0, tzinfo=UTC)

    snapshot = take_snapshot(client, SMART_LIST_NAME, None, now)

    assert (snapshot.taken_at, snapshot.list_name, snapshot.open_count, snapshot.completed_count) == (
        now,
        SMART_LIST_NAME,
        2,
        2,
    )


def test_take_snapshot_uses_completed_filter_override() -> None:
    override = "list:Inbox AND completed:today"
    client = make_client({SMART_FILTER: [], override: [make_task(True)]})

    snapshot = take_snapshot(client, SMART_LIST_NAME, override, datetime(2026, 11, 19, tzinfo=UTC))

    assert snapshot.completed_count == 1


def test_completed_today_filter_swaps_status_and_adds_suffix() -> None:
    assert completed_today_filter(SMART_FILTER) == COMPLETED_FILTER


def test_completed_today_filter_on_real_smart_list() -> None:
    smart = (
        '((list:Inbox OR list:"XIDA - Benni") AND ((status:incomplete AND (dueBefore:today OR due:never)) '
        'OR dueWithin:"1 days of today") AND isSubtask:false AND NOT (tag:"waitingforsomething"))'
    )
    expected = (
        '(((list:Inbox OR list:"XIDA - Benni") AND ((status:completed AND (dueBefore:today OR due:never)) '
        'OR dueWithin:"1 days of today") AND isSubtask:false AND NOT (tag:"waitingforsomething"))) '
        "AND completed:today"
    )
    assert completed_today_filter(smart) == expected


def test_completed_today_filter_without_status_only_adds_suffix() -> None:
    assert completed_today_filter("list:Inbox") == "(list:Inbox) AND completed:today"
