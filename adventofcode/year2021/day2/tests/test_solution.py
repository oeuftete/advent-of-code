import pytest

from adventofcode.year2021.day2.solution import Positionator


@pytest.fixture(name="example_course")
def fixture_example_course():
    return [
        "forward 5",
        "down 5",
        "forward 8",
        "up 3",
        "down 8",
        "forward 2",
    ]


def test_product_position(example_course):
    assert Positionator(example_course).position_product == 150


def test_product_aim(example_course):
    assert Positionator(example_course, course_type="aim").position_product == 900
