import pytest

from adventofcode.year2022.day3.solution import RucksackCollection


@pytest.fixture(name="example_rucksack_list")
def fixture_example_rucksack_list() -> list[str]:
    return """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""".strip().splitlines()


def test_rucksack_collection(example_rucksack_list):
    rc = RucksackCollection(example_rucksack_list)

    assert len(rc.rucksacks) == 6
    assert rc.rucksacks[0].common_item == "p"
    assert rc.rucksacks[0].common_item_priority == 16
    assert rc.priority_sum == 157
    assert rc.rearrangement_sum == 70
