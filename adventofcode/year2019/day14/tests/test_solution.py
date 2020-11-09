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


@pytest.fixture
def reaction_three():
    return """
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
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
    assert factory.g.nodes["A"]["reserve"] == 2
    assert factory.g.nodes["B"]["reserve"] == 0


def test_reaction_two(reaction_two):
    factory = Nanofactory(reaction_two)
    assert factory.minimum_ore == 165
    assert factory.g.nodes["A"]["reserve"] == 0
    assert factory.g.nodes["B"]["reserve"] == 1
    assert factory.g.nodes["C"]["reserve"] == 3


@pytest.mark.xfail
def test_reaction_three(reaction_three):
    factory = Nanofactory(reaction_three)
    assert factory.minimum_ore == 13312
