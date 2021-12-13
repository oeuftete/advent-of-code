import logging
from collections import Counter

import attr
import networkx as nx  # type: ignore
from aocd.models import Puzzle  # type: ignore

LOGGER = logging.getLogger("solveaocd")
logging.basicConfig(level=logging.DEBUG)


@attr.s
class Cavern:
    raw_paths: list[str] = attr.ib()
    revisit_small_caves: bool = attr.ib(default=False)
    g: nx.DiGraph = attr.ib(init=False, factory=nx.DiGraph)
    possible_paths: set[tuple] = attr.ib(init=False, factory=set)

    def __attrs_post_init__(self) -> None:
        #  For each edge in the input, add the edge and -- if it's not terminal
        #  -- add the converse.
        for edge in [tuple(e.split("-")) for e in self.raw_paths]:

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
        #  make a copy of each edge with UPPER replaced by UPPER_lower.  If
        #  we're allowing one small node revisit, make one additional copy.
        for n in list(filter(lambda s: s.isupper(), self.g.nodes)):
            for lower_node in [e[1] for e in self.g.edges(n) if e[1] != "end"]:
                dup_node = f"{n}_{lower_node}"

                for edge in self.g.in_edges(n):
                    LOGGER.debug("Adding UPPER dup (in) edge: %s", (edge[0], dup_node))
                    self.g.add_edge(edge[0], dup_node)
                    if self.revisit_small_caves:
                        self.g.add_edge(edge[0], f"{dup_node}2")

                for edge in self.g.out_edges(n):
                    LOGGER.debug("Adding UPPER dup (out) edge: %s", (dup_node, edge[1]))
                    self.g.add_edge(dup_node, edge[1])
                    self.g.add_edge(f"{dup_node}2", edge[1])

        #  If lower nodes can be revisited once, add one duplicate node for
        #  each lower-case node.
        if self.revisit_small_caves:
            for n in list(
                filter(
                    lambda s: s.islower() and s not in ["start", "end"], self.g.nodes
                )
            ):
                dup_node = f"{n}_dup"
                for edge in self.g.in_edges(n):
                    LOGGER.debug(
                        "Adding _lower_ dup (in) edge: %s", (edge[0], dup_node)
                    )
                    self.g.add_edge(edge[0], dup_node)

                for edge in self.g.out_edges(n):
                    LOGGER.debug(
                        "Adding _lower_ dup (out) edge: %s", (dup_node, edge[1])
                    )
                    self.g.add_edge(dup_node, edge[1])

        def _has_duplicate_lower(p) -> bool:
            counter = Counter(
                filter(
                    lambda c: c.islower() and c not in ["start", "end"],
                    p,
                ),
            )
            LOGGER.debug("Counter: %s", counter)
            if len(counter) > 1 and counter.most_common(2)[1][1] > 1:
                LOGGER.debug("Discarded path for lower dup: %s", p)
                return True
            return False

        def _normalized_path(p) -> tuple:
            return p

        #  If there are more than two lower-case nodes with two entries, discard
        #  Get all possible simple paths, normalizing all _lower-suffixed nodes.
        #  self.possible_paths = {
        #      tuple(map(lambda s: s.split("_")[0], p))
        #      for p in nx.all_simple_paths(self.g, source="start", target="end")
        #  }

        seen_paths = set()
        for p in nx.all_simple_paths(self.g, source="start", target="end"):
            path = tuple(map(lambda s: s.split("_")[0], p))
            if path in seen_paths:
                continue
            seen_paths.add(path)

            if self.revisit_small_caves and _has_duplicate_lower(path):
                LOGGER.debug("Discarded lower-dup possible path: %s", path)
                continue

            LOGGER.debug("Adding possible path: %s", path)
            self.possible_paths.add(path)

        #  if self.revisit_small_caves:
        #      self.possible_paths = set(filter(_has_duplicate_lower, self.possible_paths))

        LOGGER.debug("All paths:")
        for p in sorted(self.possible_paths):
            LOGGER.debug("  %s", p)


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=12)
    lines = puzzle.input_data.strip().splitlines()

    #  puzzle.answer_a = len(Cavern(lines).possible_paths)
    puzzle.answer_b = len(Cavern(lines, revisit_small_caves=True).possible_paths)
