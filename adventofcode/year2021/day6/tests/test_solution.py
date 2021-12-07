import pytest

from adventofcode.year2021.day6.solution import School


@pytest.fixture(name="initial_lanternfish")
def fixture_initial_lanternfish():
    return "3,4,3,1,2".split(",")


def test_initial_lanternfish(initial_lanternfish):
    school = School(initial_lanternfish)

    school.age(1)
    assert school.fish == [2, 3, 2, 0, 1]

    school.age(1)
    assert school.fish == [1, 2, 1, 6, 0, 8]

    school.age(16)
    assert school.fish == [
        6,
        0,
        6,
        4,
        5,
        6,
        0,
        1,
        1,
        2,
        6,
        0,
        1,
        1,
        1,
        2,
        2,
        3,
        3,
        4,
        6,
        7,
        8,
        8,
        8,
        8,
    ]
    assert len(school.fish) == 26

    school.age(62)
    assert len(school.fish) == 5934


def test_initial_lanternfish_smart(initial_lanternfish):
    school = School(initial_lanternfish)
    assert school.fish_counter.total() == 5

    school.smart_age(1)
    assert school.fish_counter[2] == 2
    assert school.fish_counter[3] == 1
    assert school.fish_counter[4] == 0
    assert school.fish_counter.total() == 5

    school.smart_age(1)
    assert school.fish_counter[0] == 1
    assert school.fish_counter[1] == 2
    assert school.fish_counter[8] == 1
    assert school.fish_counter.total() == 6

    school.smart_age(16)
    assert school.fish_counter.total() == 26

    school.smart_age(62)
    assert school.fish_counter.total() == 5934
