import pytest

from adventofcode.year2021.day9.solution import HeightMap


@pytest.fixture(name="example_lines")
def fixture_example_lines():
    return """
2199943210
3987894921
9856789892
8767896789
9899965678
""".strip().splitlines()


def test_example_lines(example_lines):
    hm = HeightMap(example_lines)

    assert len(hm.low_points) == 4
    assert hm.risk_level_sum == 15
