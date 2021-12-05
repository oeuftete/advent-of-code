import pytest

from adventofcode.common.coordinate import Coordinate
from adventofcode.year2021.day5.solution import VentMap


@pytest.fixture(name="example_lines")
def fixture_example_lines():
    return """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""".strip().splitlines()


def test_example_lines(example_lines):
    vm = VentMap(lines=example_lines)

    assert vm.grid[Coordinate(0, 0)] == 0
    assert vm.grid[Coordinate(2, 1)] == 1
    assert vm.grid[Coordinate(4, 4)] == 1
    assert vm.grid[Coordinate(0, 9)] == 2

    assert len(vm.danger_spots) == 5


def test_example_lines_with_diagonals(example_lines):
    vm = VentMap(lines=example_lines, check_diagonals=True)

    assert vm.grid[Coordinate(0, 0)] == 1
    assert vm.grid[Coordinate(2, 1)] == 1
    assert vm.grid[Coordinate(4, 4)] == 3
    assert vm.grid[Coordinate(0, 9)] == 2

    assert len(vm.danger_spots) == 12
