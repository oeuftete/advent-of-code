import pytest

from adventofcode.year2018.day18.solution import (
    Lumberyard,
    LUMBERYARD,
    OPEN_SPACE,
    TREES,
)


@pytest.fixture
def sample_yard():
    return Lumberyard(
        """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
""".strip()
    )


@pytest.mark.parametrize(
    "x,y,s,empty,tree,yard",
    [
        (0, 0, OPEN_SPACE, True, False, False),
        (3, 0, LUMBERYARD, False, False, True),
        (7, 0, TREES, False, True, False),
        (5, 5, TREES, False, True, False),
        (9, 9, OPEN_SPACE, True, False, False),
    ],
)
def test_grid_parse(sample_yard, x, y, s, empty, tree, yard):
    assert sample_yard.grid[x][y] == s
    assert sample_yard.is_open(x, y) == empty
    assert sample_yard.is_trees(x, y) == tree
    assert sample_yard.is_lumberyard(x, y) == yard

    assert sample_yard.x_size == 10
    assert sample_yard.y_size == 10


@pytest.mark.parametrize(
    "x,y,n",
    [(0, 0, 3), (3, 0, 5), (0, 3, 5), (9, 3, 5), (5, 5, 8), (9, 0, 3), (9, 9, 3),],
)
def test_adjacency(sample_yard, x, y, n):
    assert len(sample_yard.adjacent_points(x, y)) == n


@pytest.mark.parametrize(
    "x,y,s,empty,tree,yard,i",
    [
        (0, 0, OPEN_SPACE, True, False, False, 1),
        (3, 0, OPEN_SPACE, True, False, False, 1),
        (7, 0, LUMBERYARD, False, False, True, 1),
        (5, 5, TREES, False, True, False, 1),
        (9, 9, OPEN_SPACE, True, False, False, 1),
        (0, 0, OPEN_SPACE, True, False, False, 10),
        (3, 0, LUMBERYARD, False, False, True, 10),
        (7, 0, OPEN_SPACE, True, False, False, 10),
        (5, 5, OPEN_SPACE, True, False, False, 10),
        (9, 9, TREES, False, True, False, 10),
    ],
)
def test_iteration(sample_yard, x, y, s, empty, tree, yard, i):
    sample_yard.iterate(i)

    assert sample_yard.grid[x][y] == s
    assert sample_yard.is_open(x, y) == empty
    assert sample_yard.is_trees(x, y) == tree
    assert sample_yard.is_lumberyard(x, y) == yard


def test_value(sample_yard):
    assert sample_yard.iterate(10).value == 1147
