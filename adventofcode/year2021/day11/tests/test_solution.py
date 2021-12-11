import pytest

from adventofcode.year2021.day11.solution import OctopusGrid


@pytest.fixture(name="example_small")
def fixture_example_small():
    return """
11111
19991
19191
19991
11111
""".strip().splitlines()


@pytest.fixture(name="example_large")
def fixture_example_large():
    return """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""".strip().splitlines()


def test_example_small(example_small):
    og = OctopusGrid(example_small)
    assert og.grid_size == 25

    assert og.cycle() == 9
    assert og.n_flashes == 9

    assert og.cycle() == 0
    assert og.n_flashes == 9


def test_example_large(example_large):
    og = OctopusGrid(example_large)
    assert og.grid_size == 100

    _ = og.cycle(10)
    assert og.n_flashes == 204

    _ = og.cycle(90)
    assert og.n_flashes == 1656

    og.cycle_until_all_flash()
    assert og.current_step == 195
