import logging
import re

import attr
from aocd.models import Puzzle


@attr.s
class StackMove:
    rule: str = attr.ib()
    from_stack: int = attr.ib(init=False)
    to_stack: int = attr.ib(init=False)
    n: int = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        m = re.match(r"move (\d+) from (\d+) to (\d+)$", self.rule)
        (self.n, self.from_stack, self.to_stack) = map(int, m.groups())


@attr.s
class StackManager:
    stack_definition: list[str] = attr.ib()
    stack_moves: list[StackMove] = attr.ib(factory=list, init=False)
    stacks: list[list[str]] = attr.ib(factory=list, init=False)

    def __attrs_post_init__(self) -> None:
        for l in reversed(self.stack_definition):
            logging.debug("Line: %s", l)
            if re.fullmatch(r"move.*", l):
                logging.debug("Processing move instruction")
                self.stack_moves.insert(0, StackMove(l))
            elif m := re.fullmatch(r"\s+\d.*(\d)\s*", l):
                logging.debug("Initializing stacks")
                self.stacks = [[] for _ in range(int(m.groups()[0]))]
            elif re.fullmatch(r"\s*\[.*", l):
                logging.debug("Adding row [%s] to stacks", l)
                self.add_stack_row(l)

    def add_stack_row(self, line: str) -> None:
        i = 0
        logging.debug("add_stack_row: Line: %s", line)
        while i * 4 < len(line):
            stack_entry = line[i * 4 : i * 4 + 4]
            logging.debug("  stack_entry: %s", stack_entry)
            if m := re.fullmatch(r"\s*\[(\w)\]\s*", stack_entry):
                logging.debug("  adding stack_entry %s to stack %d", m.groups()[0], i)
                self.stacks[i].append(m.groups()[0])
            i += 1

    def move(self) -> None:
        try:
            stack_move = self.stack_moves.pop(0)
        except IndexError as exc:
            raise StopIteration("No more moves!") from exc

        for _ in range(stack_move.n):
            crate = self.stacks[stack_move.from_stack - 1].pop()
            logging.debug(
                "Moving %s from stack %d to stack %d",
                crate,
                stack_move.from_stack,
                stack_move.to_stack,
            )
            self.stacks[stack_move.to_stack - 1].append(crate)

    def move_all(self) -> None:
        while True:
            try:
                self.move()
            except StopIteration:
                return

    @property
    def message(self) -> str:
        return "".join([s[-1] for s in self.stacks])


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=5)
    stack_manager = StackManager(puzzle.input_data.splitlines())
    stack_manager.move_all()
    puzzle.answer_a = stack_manager.message
