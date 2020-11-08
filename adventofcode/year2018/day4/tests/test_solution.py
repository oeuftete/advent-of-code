import pytest

from adventofcode.year2018.day4.solution import (
    parse_log_entry,
    sleepiest_guard_in_log,
    sleepiest_guard_minute_in_log,
    sorted_log_entries,
)

#  TODO: Use pytest fixture correctly
from .fixtures import sorted_guard_log, unsorted_guard_log


@pytest.mark.parametrize(
    "log,log_midnight_minute,log_date," "guard_no,is_beginning,fell_asleep,woke_up",
    [
        ("[1518-11-01 00:55] wakes up", 55, "1518-11-01", None, False, False, True),
        (
            "[1518-11-01 23:58] Guard #99 begins shift",
            None,
            "1518-11-01",
            99,
            True,
            False,
            False,
        ),
        ("[1518-11-02 00:40] falls asleep", 40, "1518-11-02", None, False, True, False),
        ("[1518-11-02 00:50] wakes up", 50, "1518-11-02", None, False, False, True),
    ],
)
def test_parse_log_entry(
    log, log_midnight_minute, log_date, guard_no, is_beginning, fell_asleep, woke_up
):
    parsed = parse_log_entry(log)
    assert parsed.log_day.midnight_minute() == log_midnight_minute
    assert parsed.log_day.date() == log_date
    assert parsed.guard_no == guard_no
    assert parsed.is_beginning == is_beginning
    assert parsed.fell_asleep == fell_asleep
    assert parsed.woke_up == woke_up


@pytest.mark.parametrize(
    "raw_log,sorted_log", [(unsorted_guard_log(), sorted_guard_log()),]
)
def test_sorted_log_entries(raw_log, sorted_log):
    assert [l.entry for l in sorted_log_entries(raw_log)] == sorted_log


@pytest.mark.parametrize(
    "log,sleepiest_guard_no,"
    "sleepiest_guard_total_minutes,"
    "sleepiest_guard_sleepy_minute,"
    "sleepiest_guard_minute_tuple",
    [(unsorted_guard_log(), 10, 50, 24, (99, 45, 3))],
)
def test_sleepiest_guard(
    log,
    sleepiest_guard_no,
    sleepiest_guard_total_minutes,
    sleepiest_guard_sleepy_minute,
    sleepiest_guard_minute_tuple,
):

    sleepiest_guard = sleepiest_guard_in_log(log)
    assert sleepiest_guard.no == sleepiest_guard_no
    assert sleepiest_guard.total_minutes() == sleepiest_guard_total_minutes
    assert sleepiest_guard.sleepy_minute() == sleepiest_guard_sleepy_minute

    assert sleepiest_guard_minute_in_log(log) == sleepiest_guard_minute_tuple
