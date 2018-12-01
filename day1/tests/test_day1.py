import os
import pytest

from day1.solution import (
    frequency_repeat_checker,
    frequency_summer,
    read_input,
)


def test_read_input():
    assert read_input(
        os.path.join(os.path.dirname(os.path.realpath(__file__)),
                     'test_input.txt')
    ) == ['-1', '+1', '-2']


@pytest.mark.parametrize("freq_deltas,expected", [
    (['+1', '+1', '+1'], 3),
    (['+1', '+1', '-2'], 0),
    (['-1', '-2', '-3'], -6)
])
def test_day1_1(freq_deltas, expected):
    assert frequency_summer(freq_deltas) == expected


@pytest.mark.parametrize("freq_deltas,expected", [
    (['+1', '-1'], 0),
    (['+3', '+3', '+4', '-2', '-4'], 10),
    (['-6', '+3', '+8', '+5', '-6'], 5),
    (['+7', '+7', '-2', '-7', '-4'], 14),
])
def test_day1_2(freq_deltas, expected):
    assert frequency_repeat_checker(freq_deltas) == expected
