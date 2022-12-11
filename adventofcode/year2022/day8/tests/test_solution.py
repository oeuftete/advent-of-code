import pytest

from adventofcode.year2022.day8.solution import TreeSpotter


@pytest.fixture(name="example_forest")
def fixture_example_forest():
    return """
30373
25512
65332
33549
35390
""".strip()


def test_example_forest(example_forest):
    tree_spotter = TreeSpotter(example_forest)

    for x in range(5):
        assert tree_spotter.tree_is_visible(x, 0)
        assert tree_spotter.tree_is_visible(x, 4)

    for y in range(1, 4):
        assert tree_spotter.tree_is_visible(0, y)
        assert tree_spotter.tree_is_visible(4, y)

    assert tree_spotter.tree_is_visible(1, 1)
    assert tree_spotter.tree_is_visible(2, 1)
    assert not tree_spotter.tree_is_visible(3, 1)

    assert tree_spotter.tree_is_visible(1, 2)
    assert not tree_spotter.tree_is_visible(2, 2)
    assert tree_spotter.tree_is_visible(3, 2)

    assert not tree_spotter.tree_is_visible(1, 3)
    assert tree_spotter.tree_is_visible(2, 3)
    assert not tree_spotter.tree_is_visible(3, 3)

    assert tree_spotter.part_a_solution == 21
