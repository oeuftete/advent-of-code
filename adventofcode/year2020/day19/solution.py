import logging
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import product

from aocd.models import Puzzle

logging.basicConfig(level=logging.INFO)


@dataclass
class SatelliteRules:
    raw_rules: list
    rules: dict = field(default_factory=dict)
    resolved_rules: dict = field(default_factory=lambda: defaultdict(list))

    def __post_init__(self):
        for raw_rule in self.raw_rules:
            rule_no, rule = raw_rule.split(": ")
            self.rules[int(rule_no)] = rule

    def resolve_rule(self, rule_no: int) -> list:
        if rule_no in self.resolved_rules and self.resolved_rules[rule_no]:
            return self.resolved_rules[rule_no]

        rule = self.rules[rule_no]
        if rule in ('"a"', '"b"'):
            self.resolved_rules[rule_no] = [rule.strip('"')]
            return self.resolved_rules[rule_no]

        potential_results = set()
        for sub_rule in rule.split(" | "):
            potential_sub_results = []
            for sub_sub_rule in sub_rule.split(" "):
                potential_sub_results.append(self.resolve_rule(int(sub_sub_rule)))

            logging.debug(
                "[%s][%s] Potential sub_results: %s",
                rule_no,
                sub_rule,
                potential_sub_results,
            )
            for p in product(*potential_sub_results):
                logging.debug("[%s][%s] Product entry: %s", rule_no, sub_rule, p)
                potential_results.add("".join(p))

        self.resolved_rules[rule_no] = list(potential_results)
        return self.resolved_rules[rule_no]

    def validate(self, message, rule_no=0) -> bool:
        return message in self.resolve_rule(rule_no)


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=19)

    rule_str, _, data_str = puzzle.input_data.partition("\n\n")
    rules = SatelliteRules(rule_str.splitlines())
    messages = data_str.splitlines()
    puzzle.answer_a = len([msg for msg in messages if rules.validate(msg)])
