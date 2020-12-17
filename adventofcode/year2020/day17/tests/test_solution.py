import pytest

from adventofcode.year2020.day17.solution import CubeCell, CubeEngine


@pytest.fixture(name="simple_initial")
def fixture_simple_initial():
    return """
.#.
..#
###
""".strip()


def test_cube_cell():
    cc = CubeCell()
    assert len(cc.neighbours) == 26
    assert (1, 1, 1) in cc.neighbours
    assert (0, 0, 0) not in cc.neighbours


def test_cube_engine(simple_initial):
    cube_engine = CubeEngine(simple_initial)
    assert cube_engine.grid[CubeCell(0, 0, 0)] == "."
    assert cube_engine.grid[CubeCell(1, 0, 0)] == "#"
    assert cube_engine.grid[CubeCell(2, 2, 0)] == "#"
    assert cube_engine.grid[CubeCell(4, 4, 4)] == "."  # default
    assert cube_engine.active_cells == 5

    cube_engine = CubeEngine(simple_initial)
    cube_engine.iterate(1)
    assert cube_engine.active_cells == 11

    cube_engine.iterate(5)
    assert cube_engine.active_cells == 112
