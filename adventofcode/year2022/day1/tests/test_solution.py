import pytest

from adventofcode.year2022.day1.solution import CalorieCounter


@pytest.fixture(name="example_lines")
def fixture_example_lines():
    return """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
""".strip()


def test_example_lines(example_lines):
    calorie_counter = CalorieCounter(example_lines)

    assert len(calorie_counter.calories) == 5
    assert calorie_counter.calories[0] == 6000
    assert calorie_counter.max_calories == 24000
    assert calorie_counter.top_three_calories == 45000
