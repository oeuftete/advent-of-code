import pytest

from adventofcode.year2017.day3.solution import SumSpiral


@pytest.mark.parametrize("square,distance", [(1, 0), (12, 3), (23, 2), (1024, 31)])
def test_steps(square, distance):
    assert SumSpiral().count_distance_to_origin(square) == distance


@pytest.mark.parametrize("value,first_larger", [(10, 11), (20, 23), (800, 806)])
def test_first_larger(value, first_larger):
    assert SumSpiral(flavour="neighbour").first_value_gt(value) == first_larger
