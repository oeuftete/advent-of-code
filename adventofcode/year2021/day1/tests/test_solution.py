import pytest

from adventofcode.year2021.day1.solution import Sonar


@pytest.mark.parametrize(
    "measurements,window_size,n_increases",
    [
        ([199, 200, 208, 210, 200, 207, 240, 269, 260, 263], 1, 7),
        ([199, 200, 208, 210, 200, 207, 240, 269, 260, 263], 3, 5),
    ],
)
def test_increases(measurements, window_size, n_increases):
    assert Sonar(measurements).n_increases(window_size=window_size) == n_increases
