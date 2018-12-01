import os
import pytest

from day1.solution import frequency_summer, read_input


def test_read_input():
    assert read_input(
        os.path.join(os.path.dirname(os.path.realpath(__file__)),
                     'test_input.txt')
    ) == ['-1', '+1', '-2']


@pytest.mark.parametrize("frequencies,expected", [
    (['+1', '+1', '+1'], 3),
    (['+1', '+1', '-2'], 0),
    (['-1', '-2', '-3'], -6)
])
def test_day1_1(frequencies, expected):
    assert frequency_summer(frequencies) == expected
