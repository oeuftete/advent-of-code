import logging
import re
from dataclasses import dataclass

import networkx
from aocd.models import Puzzle

logging.basicConfig(level=logging.INFO)


@dataclass
class BaggageRules:
    rules_text: str

    def __post_init__(self):
        # build the graph
        self.graph = networkx.DiGraph()
        for rule in self.rules_text.split("\n"):
            rule_match = re.match(r"^(.*?) bags contain (.*)\.", rule)
            rule_colour = rule_match.group(1)
            for contained in rule_match.group(2).split(", "):
                if contained == "no other bags":
                    continue

                contained_match = re.match(r"(\d+) (.*?) bags?$", contained)
                contained_number, contained_colour = contained_match.groups()
                logging.debug(
                    "Adding edge %s -> %s, weight %s",
                    rule_colour,
                    contained_colour,
                    contained_number,
                )
                self.graph.add_edge(
                    rule_colour, contained_colour, number_contained=contained_number
                )

    def can_carry(self, colour):
        """Return a list of bag colours that can hold the given one."""
        return list(networkx.dfs_predecessors(self.graph.reverse(), colour))


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=7)
    rules_text = puzzle.input_data
    puzzle.answer_a = len(BaggageRules(rules_text).can_carry("shiny gold"))
