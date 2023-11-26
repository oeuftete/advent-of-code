import pytest
from aocd.models import Puzzle

from adventofcode.year2022.day1.solution import CalorieCounter

EXAMPLE = Puzzle(year=2022, day=1).examples[0]


@pytest.fixture(name="example_lines")
def fixture_example_lines():
    return EXAMPLE.input_data


def test_example_lines(example_lines):
    calorie_counter = CalorieCounter(example_lines)

    assert len(calorie_counter.calories) == 5
    assert calorie_counter.calories[0] == 6000
    assert calorie_counter.max_calories == int(EXAMPLE.answer_a)
    assert calorie_counter.top_three_calories == int(EXAMPLE.answer_b)
