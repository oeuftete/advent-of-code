import pytest

from adventofcode.year2018.day1.solution import (
    frequency_repeat_checker,
    frequency_summer,
)


@pytest.mark.parametrize(
    "freq_deltas,expected",
    [(["+1", "+1", "+1"], 3), (["+1", "+1", "-2"], 0), (["-1", "-2", "-3"], -6)],
)
def test_day1_1(freq_deltas, expected):
    assert frequency_summer(freq_deltas) == expected


@pytest.mark.parametrize(
    "freq_deltas,expected",
    [
        (["+1", "-1"], 0),
        (["+3", "+3", "+4", "-2", "-4"], 10),
        (["-6", "+3", "+8", "+5", "-6"], 5),
        (["+7", "+7", "-2", "-7", "-4"], 14),
    ],
)
def test_day1_2(freq_deltas, expected):
    assert frequency_repeat_checker(freq_deltas) == expected
