import logging
from dataclasses import dataclass, field
from typing import Optional

from aocd.models import Puzzle

logging.basicConfig(level=logging.INFO)


@dataclass
class Equation:
    left: Optional[int] = field(default=None)
    operator: Optional[int] = field(default=None)
    right: Optional[str] = field(default=None)

    @property
    def is_complete(self):
        return all([f is not None for f in (self.left, self.operator, self.right)])

    def add_digit(self, d):
        d = int(d)
        if self.left is not None:
            self.right = d
        else:
            self.left = d

    def add_operator(self, o):
        if self.operator is not None:
            raise ValueError(f"Operator already set: {self.operator}")
        self.operator = o

    def resolve(self):
        result = (
            self.left * self.right if self.operator == "*" else self.left + self.right
        )
        self.left = result
        self.operator = self.right = None
        return result


@dataclass
class Calculator:
    equation: str

    @property
    def tokenized(self):
        return [c for c in self.equation if c != ""]

    @property
    def result(self) -> int:
        calculation = [Equation()]
        for token in self.tokenized:
            logging.debug("[%s] Adding token [%s]", len(calculation), token)
            if token == "(":
                calculation.append(Equation())
            elif token.isdigit():
                calculation[-1].add_digit(token)
            elif token in ("*", "+"):
                calculation[-1].add_operator(token)
            elif token == ")":
                deep_result = calculation.pop().left
                calculation[-1].add_digit(deep_result)

            if calculation[-1].is_complete:
                interim = calculation[-1].resolve()
                logging.debug(
                    "[%s] Calculation was complete = %s", len(calculation), interim
                )
            logging.debug("[%s] Resulting calcs: %s", len(calculation), calculation)

        return calculation[-1].left


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=18)
    homework = puzzle.input_data.strip().splitlines()
    puzzle.answer_a = sum([Calculator(equation).result for equation in homework])
