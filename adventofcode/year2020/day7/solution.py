import logging
import re
from dataclasses import dataclass

import networkx as nx
from aocd.models import Puzzle

logging.basicConfig(level=logging.INFO)


@dataclass
class BaggageRules:
    rules_text: str

    def __post_init__(self):
        # build the graph
        self.graph = nx.DiGraph()
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
                    rule_colour,
                    contained_colour,
                    number_contained=int(contained_number),
                )

    def can_carry(self, colour):
        """Return a list of bag colours that can hold the given one."""
        return list(nx.dfs_predecessors(self.graph.reverse(), colour))

    def contained_bags(self, colour):
        colour_graph = self.graph.subgraph(
            [colour, *list(nx.dfs_predecessors(self.graph, colour))]
        )
        logging.debug("Looking at colour [%s]", colour)
        number_contained = 0

        for edge in colour_graph.edges(colour, data=True):
            _, next_colour, edge_data = edge
            colour_contained = edge_data["number_contained"]
            logging.debug(
                "Looking at colour [%s]: need [%s] (%s)",
                colour,
                next_colour,
                colour_contained,
            )

            #  We need this many of this bag...
            number_contained += colour_contained

            #  ... plus that many of however many contained bags there are
            number_contained += self.contained_bags(next_colour) * colour_contained

        logging.debug("Looking at colour [%s]: returning: %s", colour, number_contained)
        return number_contained


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=7)
    rules_text = puzzle.input_data
    puzzle.answer_a = len(BaggageRules(rules_text).can_carry("shiny gold"))
    puzzle.answer_b = BaggageRules(rules_text).contained_bags("shiny gold")
