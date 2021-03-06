import pytest

from adventofcode.year2020.day7.solution import BaggageRules


@pytest.fixture(name="sample_rules")
def fixture_sample_rules():
    return """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""".strip()


@pytest.fixture(name="harder_rules")
def fixture_harder_rules():
    return """
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
""".strip()


def test_baggage_rules(sample_rules, harder_rules):
    baggage_rules = BaggageRules(sample_rules)
    shiny_gold_holders = baggage_rules.can_carry("shiny gold")
    assert len(shiny_gold_holders) == 4
    assert sorted(shiny_gold_holders) == sorted(
        [
            "bright white",
            "muted yellow",
            "dark orange",
            "light red",
        ]
    )
    assert baggage_rules.contained_bags("shiny gold") == 32
    assert BaggageRules(harder_rules).contained_bags("shiny gold") == 126
