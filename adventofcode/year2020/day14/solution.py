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
    version: int = 1
    mask: str = "0" * 36
    memory: dict = field(default_factory=lambda: defaultdict(empty_bitarray))

    def memset_v1(self, address, value):
        and_mask = ba(self.mask.replace("X", "1"))
        or_mask = ba(self.mask.replace("X", "0"))

        self.memory[address] = int2ba(int(value), length=36) & and_mask | or_mask

    def memset_v2(self, address, value):
        #  All 0's don't change, so just ignore those.
        #  All 1's set to 1.
        one_or_mask = ba(self.mask.replace("X", "0"))
        base_address = int2ba(int(address), length=36) | one_or_mask

        #  All X's are "floating"
        all_addresses = [base_address]
        x_indices = [i for i, b in enumerate(self.mask, start=1) if b == "X"]
        for xi in x_indices:
            for a in all_addresses.copy():
                all_addresses.append(a ^ int2ba(1 << (36 - xi), length=36))

        for a in all_addresses:
            self.memory[ba2int(a)] = int2ba(int(value), length=36)

    def process(self):
        while self.instructions:
            instruction = self.instructions.pop(0)
            action, value = instruction.split(" = ")
            if action == "mask":
                self.mask = value
            elif action.startswith("mem"):
                match = re.match(r"mem\[(\d+)\]", action)
                address = int(match.groups()[0])
                if self.version == 1:
                    self.memset_v1(address, value)
                else:
                    self.memset_v2(address, value)

            logging.debug("Memory contents: %s", self.memory)

    def sum_memory(self):
        return sum([ba2int(v) for v in self.memory.values()])


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=14)
    instructions = puzzle.input_data.strip().splitlines()
    computer = SeaportComputer(instructions.copy())
    computer.process()

    puzzle.answer_a = computer.sum_memory()

    v2_computer = SeaportComputer(instructions, version=2)
    v2_computer.process()

    puzzle.answer_b = v2_computer.sum_memory()
