import pytest

from adventofcode.year2022.day2.solution import StrategyGuide


@pytest.fixture(name="example_lines")
def fixture_example_lines():
    return """
A Y
B X
C Z
""".strip()


def test_example_lines(example_lines):
    strategy_guide = StrategyGuide(example_lines)

    assert len(strategy_guide.game_scores) == 3
    assert strategy_guide.game_scores == [8, 1, 6]
    assert strategy_guide.total_score == 15
