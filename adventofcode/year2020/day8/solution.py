from dataclasses import dataclass, field

from aocd.models import Puzzle


@dataclass
class ConsoleComputer:
    code: str
    accumulator: int = field(default=0, init=False)
    address: int = field(default=0, init=False)
    visited: set = field(default_factory=list, init=False)
    rules: list = field(default_factory=list, init=False)

    def __post_init__(self):
        for line in self.code.strip().split("\n"):
            instruction, value = line.split(" ")
            self.rules.append((instruction, int(value)))

    def run_until_loop(self):
        while True:
            if self.address in self.visited:
                break

            self.visited.append(self.address)

            instruction, value = self.rules[self.address]
            if instruction == "nop":
                self.address += 1
            elif instruction == "acc":
                self.address += 1
                self.accumulator += value
            elif instruction == "jmp":
                self.address += value
            else:
                raise ValueError(f"Unknown instruction {instruction}!")


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=8)
    computer = ConsoleComputer(puzzle.input_data)
    computer.run_until_loop()
    puzzle.answer_a = computer.accumulator
