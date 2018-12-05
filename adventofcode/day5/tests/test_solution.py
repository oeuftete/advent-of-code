import pytest

from adventofcode.day5.solution import (
    reacted_polymer
)


@pytest.mark.parametrize("polymer,reacted", [
    ('dabAcCaCBAcCcaDA', 'dabCBAcaDA'),
])
def test_reacted_polymer(polymer, reacted):
    assert reacted_polymer(polymer) == reacted
