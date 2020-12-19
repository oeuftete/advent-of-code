import pytest

from adventofcode.year2020.day19.solution import SatelliteRules


@pytest.fixture(name="simple_rules")
def fixture_simple_rules():
    return """
0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"
""".strip().splitlines()


@pytest.fixture(name="interesting_rules")
def fixture_interesting_rules():
    return """
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
""".strip().splitlines()


def test_simple_rules(simple_rules):
    rules = SatelliteRules(simple_rules)

    assert rules.resolve_rule(1) == ["a"]
    assert rules.resolve_rule(3) == ["b"]
    assert sorted(rules.resolve_rule(2)) == sorted(["ab", "ba"])
    assert rules.validate("a", 1)
    assert rules.validate("b", 3)

    assert rules.validate("ab", 2)
    assert rules.validate("ba", 2)
    assert not rules.validate("aa", 2)

    assert rules.validate("aba")
    assert rules.validate("aab")
    assert not rules.validate("ab")
    assert not rules.validate("abb")
    assert not rules.validate("abab")


def test_interesting_rules(interesting_rules):
    rules = SatelliteRules(interesting_rules)
    assert rules.validate("a", 4)
    assert rules.validate("b", 5)

    assert rules.validate("ababbb")
    assert rules.validate("abbbab")
    assert not rules.validate("bababa")
    assert not rules.validate("aaabbb")
    assert not rules.validate("aaaabbb")
