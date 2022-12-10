import logging
from functools import cached_property
from uuid import UUID, uuid4

import attr
import networkx as nx
from aocd.models import Puzzle
from networkx import DiGraph

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger = logging.getLogger("solveaocd")
logger.addHandler(ch)


@attr.s(frozen=True)
class Inode:
    name: str = attr.ib()
    is_directory: bool = attr.ib(default=False)
    size: int = attr.ib(default=0)
    uuid: UUID = attr.ib(factory=uuid4, init=False)


@attr.s
class DirReader:
    commands: list[str] = attr.ib()
    tree: DiGraph = attr.ib(factory=DiGraph, init=False)
    pwd: Inode = attr.ib(default=Inode("/", is_directory=True), init=False)

    def _safe_add_node(self, inode: Inode) -> Inode:
        # If there is an already an edge from this directory to the parent, then
        # don't add a new node.
        existing_nodes = [
            n[1]
            for n in filter(
                lambda n: n[1].name == inode.name, self.tree.edges([self.pwd])
            )
        ]

        if len(existing_nodes):
            return existing_nodes[0]

        self.tree.add_node(inode)
        return inode

    def __attrs_post_init__(self) -> None:
        self.tree.add_node(self.pwd)
        for c in self.commands:
            logger.debug("Processing command %s in pwd %s", c, self.pwd)
            match (c[0:4]):
                case "$ cd":
                    dir_name = c[5:].strip()

                    if dir_name == "..":
                        try:
                            logger.debug(
                                "Parent edges for %s are %s",
                                self.pwd.name,
                                list(
                                    filter(
                                        lambda edge: edge[1] == self.pwd,
                                        list(self.tree.edges),
                                    )
                                ),
                            )
                            self.pwd = next(
                                filter(
                                    lambda edge: edge[1] == self.pwd,
                                    list(self.tree.edges),
                                )
                            )[0]
                        except StopIteration:
                            logger.error("Couldn't find parent of %s", self.pwd)
                            raise
                    else:
                        inode = Inode(dir_name, is_directory=True)
                        self.pwd = self._safe_add_node(inode)

                case "$ ls":
                    pass
                case "dir ":
                    inode = Inode(c[4:].strip(), is_directory=True)
                    self._safe_add_node(inode)
                    logger.debug("Adding dir [%s] under [%s]", inode, self.pwd)
                    self.tree.add_edge(self.pwd, inode)
                case _:
                    (fsize, fname) = c.strip().split()
                    inode = Inode(fname, size=int(fsize))
                    self._safe_add_node(inode)
                    logger.debug("Adding file [%s] under [%s]", inode, self.pwd)
                    self.tree.add_edge(self.pwd, inode)

    def dir_size(self, inode: Inode) -> int:
        dir_nodes = nx.descendants(self.tree, inode)
        return sum(inode.size for inode in dir_nodes)

    @cached_property
    def part_a_solution(self) -> int:
        return sum(
            (
                self.dir_size(inode)
                for inode in filter(
                    lambda inode: inode.is_directory
                    and self.dir_size(inode) <= 100_000,
                    nx.nodes(self.tree),
                )
            )
        )


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=7)
    dir_reader = DirReader(puzzle.input_data.strip().splitlines())
    puzzle.answer_a = dir_reader.part_a_solution
