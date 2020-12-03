import pytest

from adventofcode.year2020.day3.solution import TreedSlope


@pytest.fixture
def example_slope():
    return """
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
""".strip()


def test_slope(example_slope):
    treed_slope = TreedSlope(example_slope)

    assert treed_slope.width == 11
    assert treed_slope.height == 11

    #  Base
    assert treed_slope.is_tree_at(0, 0) == False
    assert treed_slope.is_tree_at(0, 1) == True
    assert treed_slope.is_tree_at(0, 10) == False
    assert treed_slope.is_tree_at(1, 0) == False
    assert treed_slope.is_tree_at(1, 1) == False

    # Extended
    assert treed_slope.is_tree_at(11, 0) == False
    assert treed_slope.is_tree_at(11, 1) == True
    assert treed_slope.is_tree_at(22, 0) == False

    # Outside
    with pytest.raises(ValueError):
        treed_slope.is_tree_at(0, 11)

    treed_slope.slide()  # wheeeeee
    assert treed_slope.trees_hit == 7

    treed_slope.go_back_to_the_top()
    treed_slope.slide(1, 1)
    assert treed_slope.trees_hit == 2

    treed_slope.go_back_to_the_top()
    treed_slope.slide(5, 1)
    assert treed_slope.trees_hit == 3

    treed_slope.go_back_to_the_top()
    treed_slope.multiple_slide_product([(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]) == 336
