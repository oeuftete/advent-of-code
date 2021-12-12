import logging

import attr
import networkx as nx  # type: ignore
from aocd.models import Puzzle  # type: ignore

LOGGER = logging.getLogger("solveaocd")


@attr.s
class Cavern:
    raw_paths: list[str] = attr.ib()
    g: nx.DiGraph = attr.ib(init=False, factory=nx.DiGraph)
    possible_paths: set[tuple] = attr.ib(init=False, factory=set)

    def __attrs_post_init__(self) -> None:
        #  For each edge in the input, add the edge and -- if it's not terminal
        #  -- add the converse.
        for edge in [e.split("-") for e in self.raw_paths]:

            #  Make sure we have the direction right for terminals
            if edge[0] == "end" or edge[1] == "start":
                edge = tuple(reversed(edge))

            LOGGER.debug("Adding edge: %s", edge)
            self.g.add_edge(*edge)
            if "start" not in edge and "end" not in edge:
                rev = tuple(reversed(edge))
                LOGGER.debug("Adding reversed edge: %s", rev)
                self.g.add_edge(*rev)

        #  For each UPPER node in the input, for each lower node that is an edge,
        #  make a copy of each edge with UPPER replaced by UPPER_lower.
        for n in list(filter(lambda s: s.isupper(), self.g.nodes)):
            for lower_node in [e[1] for e in self.g.edges(n) if e[1] != "end"]:
                dup_node = f"{n}_{lower_node}"

                for edge in self.g.in_edges(n):
                    LOGGER.debug("Adding edge: %s, %s", edge[0], dup_node)
                    self.g.add_edge(edge[0], dup_node)

                for edge in self.g.out_edges(n):
                    LOGGER.debug("Adding edge: %s, %s", dup_node, edge[1])
                    self.g.add_edge(dup_node, edge[1])

        #  Get all possible simple paths, normalizing all _lower-suffixed nodes.
        self.possible_paths = {
            tuple(map(lambda s: s.split("_")[0], p))
            for p in nx.all_simple_paths(self.g, source="start", target="end")
        }


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=12)
    lines = puzzle.input_data.strip().splitlines()

    puzzle.answer_a = len(Cavern(lines).possible_paths)
