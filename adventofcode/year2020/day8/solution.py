import logging
from dataclasses import dataclass, field

from aocd.models import Puzzle

logging.basicConfig(level=logging.INFO)


class ExecutionCompleted(Exception):
    pass


@dataclass
class ConsoleComputer:
    code: str = ""
    rules: list = field(default_factory=list)
    accumulator: int = field(default=0, init=False)
    address: int = field(default=0, init=False)
    visited: set = field(default_factory=list, init=False)

    def __post_init__(self):
        if not self.rules:
            for line in self.code.strip().split("\n"):
                instruction, value = line.split(" ")
                self.rules.append((instruction, int(value)))

    def reset(self):
        self.address = 0
        self.accumulator = 0
        self.visited = []

    def run_until_loop(self):
        try:
            self.run()
        except StopIteration:
            return

        raise ExecutionCompleted("No loop found.")

    def run(self):
        while True:
            if self.address in self.visited:
                raise StopIteration

            try:
                instruction, value = self.rules[self.address]
            except IndexError:
                break

            self.visited.append(self.address)
            if instruction == "nop":
                self.address += 1
            elif instruction == "acc":
                self.address += 1
                self.accumulator += value
            elif instruction == "jmp":
                self.address += value
            else:
                raise ValueError(f"Unknown instruction {instruction}!")

    @property
    def run_with_toggles_accumulator(self):
        for i, instruction_tuple in enumerate(self.rules):
            instruction, value = instruction_tuple
            if instruction in ["nop", "jmp"]:
                logging.debug("Swapping rule [%s]", i)
                modified_rules = self.rules.copy()
                modified_rules[i] = (
                    ("nop", value) if instruction == "jmp" else ("jmp", value)
                )
                modified_computer = ConsoleComputer(rules=modified_rules)
                try:
                    modified_computer.run()
                    return modified_computer.accumulator
                except StopIteration:
                    logging.debug("Found cycle with rule [%s]", i)
                    continue

        raise ValueError("No run completed.")


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=8)
    computer = ConsoleComputer(puzzle.input_data)
    computer.run_until_loop()
    puzzle.answer_a = computer.accumulator

    computer.reset()
    puzzle.answer_b = computer.run_with_toggles_accumulator
