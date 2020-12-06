import pytest

from adventofcode.year2020.day3.solution import TreedSlope


@pytest.fixture(name="example_slope")
def fixture_example_slope():
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
    assert not treed_slope.is_tree_at(0, 0)
    assert treed_slope.is_tree_at(0, 1)
    assert not treed_slope.is_tree_at(0, 10)
    assert not treed_slope.is_tree_at(1, 0)
    assert not treed_slope.is_tree_at(1, 1)

    # Extended
    assert not treed_slope.is_tree_at(11, 0)
    assert treed_slope.is_tree_at(11, 1)
    assert not treed_slope.is_tree_at(22, 0)

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
    assert (
        treed_slope.multiple_slide_product([(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)])
        == 336
    )
