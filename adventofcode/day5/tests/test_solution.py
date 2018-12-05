import pytest

from adventofcode.day5.solution import (
    reacted_polymer,
    reduced_reacted_polymer,
    shortest_reduced_polymer
)


TEST_POLYMER = 'dabAcCaCBAcCcaDA'


@pytest.mark.parametrize("polymer,reacted", [
    (TEST_POLYMER, 'dabCBAcaDA'),
])
def test_reacted_polymer(polymer, reacted):
    assert reacted_polymer(polymer) == reacted


@pytest.mark.parametrize("polymer,bad_unit,reacted_length", [
    (TEST_POLYMER, 'a', 6),
    (TEST_POLYMER, 'b', 8),
    (TEST_POLYMER, 'c', 4),
    (TEST_POLYMER, 'd', 6),
])
def test_reduced_reacted_polymer(polymer, bad_unit, reacted_length):
    assert len(reduced_reacted_polymer(polymer, bad_unit)) == reacted_length


@pytest.mark.parametrize("polymer,bad_units,reacted_length", [
    (TEST_POLYMER, 'abcd', 4),
])
def test_shortest_reduced_polymer(polymer, bad_units, reacted_length):
    assert shortest_reduced_polymer(polymer, bad_units) == reacted_length
