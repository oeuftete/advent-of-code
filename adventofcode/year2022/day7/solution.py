import logging
from functools import cached_property
from uuid import UUID, uuid4

import attr
import networkx as nx
from aocd.models import Puzzle
from networkx import DiGraph

logging.basicConfig(level=logging.DEBUG)


@attr.s(frozen=True)
class Inode:
    name: str = attr.ib()
    is_directory: bool = attr.ib(default=False)
    size: int = attr.ib(default=0)
    uuid: UUID = attr.ib(factory=uuid4, init=False)

    def __str__(self):
        return (
            f'{self.name}{"/" if self.is_directory and self.name[-1] != "/" else ""}'
            f'{"" if self.is_directory else f" ({self.size})"}'
        )

    def __repr__(self):
        return self.__str__()


@attr.s
class DirReader:
    commands: list[str] = attr.ib()
    tree: DiGraph = attr.ib(factory=DiGraph, init=False)
    root: Inode = attr.ib(default=Inode("/", is_directory=True), init=False)
    pwd: Inode = attr.ib(init=False)

    def _safe_add_node(self, inode: Inode) -> Inode:
        # If there is an already an edge from this directory to the parent, then
        # don't add a new node.

        if inode.name == "/":
            return self.root

        existing_nodes = [
            n[1] for n in self.tree.edges([self.pwd]) if n[1].name == inode.name
        ]

        if len(existing_nodes):
            return existing_nodes[0]

        self.tree.add_node(inode)
        return inode

    def __attrs_post_init__(self) -> None:
        self.tree.add_node(self.root)
        self.pwd = self.root

        for c in self.commands:
            logging.debug("Processing command %s in pwd %s", c, self.pwd)
            match (c[0:4]):
                case "$ cd":
                    dir_name = c[5:].strip()

                    if dir_name == "..":
                        try:
                            parents = [
                                edge[0]
                                for edge in self.tree.edges
                                if edge[1] == self.pwd
                            ]
                            logging.debug("Parents of %s: %s", self.pwd, parents)
                            assert len(parents) == 1
                            self.pwd = parents[0]
                        except AssertionError:
                            logging.error("Couldn't find parent of %s", self.pwd)
                            raise
                    else:
                        inode = Inode(dir_name, is_directory=True)
                        self.pwd = self._safe_add_node(inode)

                case "$ ls":
                    pass

                case "dir ":
                    inode = Inode(c[4:].strip(), is_directory=True)
                    self._safe_add_node(inode)
                    logging.debug("Adding dir [%s] under [%s]", inode, self.pwd)
                    self.tree.add_edge(self.pwd, inode)

                case _:
                    (fsize, fname) = c.strip().split()
                    inode = Inode(fname, size=int(fsize))
                    self._safe_add_node(inode)
                    logging.debug("Adding file [%s] under [%s]", inode, self.pwd)
                    self.tree.add_edge(self.pwd, inode)

    def find_inode(self, path: list[str]) -> Inode:
        found = self.root
        for p in path:
            # find edge from current found to one named p
            try:
                found = next(
                    (e[1] for e in nx.edges(self.tree, [found]) if e[1].name == p)
                )
            except StopIteration:
                return None

        return found

    def dir_size(self, inode: Inode) -> int:
        dir_nodes = nx.descendants(self.tree, inode)
        return sum(inode.size for inode in dir_nodes)

    def node_dir_sizes(self) -> list[int]:
        return sorted((self.dir_size(n) for n in nx.nodes(self.tree) if n.is_directory))

    @cached_property
    def part_a_solution(self) -> int:
        """
        Find all of the directories with a total size of at most 100000. What is
        the sum of the total sizes of those directories?
        """
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

    @cached_property
    def part_b_solution(self) -> int:
        """
        The total disk space available to the filesystem is 70000000. To run the
        update, you need unused space of at least 30000000. You need to find
        a directory you can delete that will free up enough space to run the
        update.

        Find the smallest directory that, if deleted, would free up enough space
        on the filesystem to run the update.
        """

        free_space = 70000000 - self.dir_size(self.root)
        space_to_free = 30000000 - free_space

        return min((ns for ns in self.node_dir_sizes() if ns > space_to_free))


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=7)
    dir_reader = DirReader(puzzle.input_data.strip().splitlines())
    puzzle.answer_a = dir_reader.part_a_solution
    puzzle.answer_b = dir_reader.part_b_solution
