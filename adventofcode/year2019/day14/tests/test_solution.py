import pytest

from adventofcode.year2019.day14.solution import Nanofactory

TEST_CASES = [
    (
        """
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
""".strip(),
        31,
    ),
    (
        """
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
""".strip(),
        165,
    ),
]


@pytest.mark.parametrize("input_data,minimum_ore", TEST_CASES)
def test_factory(input_data, minimum_ore):
    factory = Nanofactory(input_data)
    assert factory.minimum_ore == minimum_ore
