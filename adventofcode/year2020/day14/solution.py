import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field

from aocd.models import Puzzle
from bitarray import bitarray as ba
from bitarray.util import ba2int, int2ba

logging.basicConfig(level=logging.INFO)


def empty_bitarray(n=36):
    b = ba(n)
    b.setall(0)
    return b


@dataclass
class SeaportComputer:
    instructions: list
    or_mask: ba = field(default_factory=empty_bitarray)
    and_mask: ba = field(default_factory=empty_bitarray)
    memory: dict = field(default_factory=lambda: defaultdict(empty_bitarray))

    def process(self):
        while self.instructions:
            instruction = self.instructions.pop(0)
            action, value = instruction.split(" = ")
            if action == "mask":
                self.or_mask = ba(value.replace("X", "0"))
                self.and_mask = ba(value.replace("X", "1"))
            elif action.startswith("mem"):
                match = re.match(r"mem\[(\d+)\]", action)
                address = int(match.groups()[0])
                self.memory[address] = (
                    int2ba(int(value), length=36) & self.and_mask | self.or_mask
                )
            logging.debug("Memory contents: %s", self.memory)

    def sum_memory(self):
        return sum([ba2int(v) for v in self.memory.values()])


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=14)
    instructions = puzzle.input_data.strip().splitlines()
    computer = SeaportComputer(instructions)
    computer.process()

    puzzle.answer_a = computer.sum_memory()
