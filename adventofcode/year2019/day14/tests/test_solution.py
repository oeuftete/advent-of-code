import pytest

from adventofcode.year2019.day14.solution import Nanofactory


@pytest.fixture
def reaction_one():
    return """
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
""".strip()


@pytest.fixture
def reaction_two():
    return """
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
""".strip()


def test_reaction_one(reaction_one):
    factory = Nanofactory(reaction_one)

    assert len(factory.g.edges()) == 10

    assert factory.minimum_ore_for_chemical("A", 1) == 10
    factory.reset()

    assert factory.minimum_ore_for_chemical("A", 1) == 10
    factory.reset()

    assert factory.minimum_ore_for_chemical("A", 11) == 20
    factory.reset()

    assert factory.minimum_ore == 31


def test_reaction_two(reaction_two):
    factory = Nanofactory(reaction_two)

    #  assert factory.minimum_ore_for_chemical("A", 1) == 9
    #  factory.reset()
    #  assert factory.minimum_ore_for_chemical("A", 2) == 9
    #  factory.reset()
    #  assert factory.minimum_ore_for_chemical("A", 3) == 18
    #  factory.reset()

    assert factory.minimum_ore == 165
