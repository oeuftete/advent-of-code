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
        if self.operator:
            result = (
                self.left * self.right
                if self.operator == "*"
                else self.left + self.right
            )
            self.left = result
            self.operator = self.right = None
        return self.left


@dataclass
class Calculator:
    equation: str

    @property
    def tokenized(self):
        return [c for c in self.equation if c != " "]

    @property
    def result(self) -> int:
        calculation = [Equation()]
        for token in self.tokenized:
            logging.debug("[%s] Adding token [%s]", len(calculation), token)
            current_eq = calculation[-1]
            if token == "(":
                calculation.append(Equation())
                current_eq = calculation[-1]
            elif token.isdigit():
                current_eq.add_digit(token)
            elif token in ("*", "+"):
                current_eq.add_operator(token)
            elif token == ")":
                deep_result = calculation.pop().left
                current_eq = calculation[-1]
                current_eq.add_digit(deep_result)

            if current_eq.is_complete:
                interim = current_eq.resolve()
                logging.debug(
                    "[%s] Calculation was complete = %s", len(calculation), interim
                )
            logging.debug("[%s] Resulting calcs: %s", len(calculation), calculation)

        logging.debug("[%s] ### Final equation: %s", len(calculation), current_eq)
        return current_eq.left

    @property
    def advanced_result(self) -> int:
        calculation = [Equation()]

        open_parens = []
        for token in self.tokenized:
            logging.debug("[%s] Adding token [%s]", len(calculation), token)
            current_eq = calculation[-1]
            if token == "(":
                calculation.append(Equation())
                current_eq = calculation[-1]
                open_parens.append(len(calculation))
            elif token.isdigit():
                #  If currently multiplying, start a new level
                if current_eq.operator == "*":
                    calculation.append(Equation())
                    current_eq = calculation[-1]
                current_eq.add_digit(token)
            elif token in ("*", "+"):
                current_eq.add_operator(token)
            elif token == ")":
                #  Resolve back to open paren
                open_paren_level = open_parens.pop()
                while len(calculation) > open_paren_level:
                    deep_result = calculation.pop().resolve()
                    current_eq = calculation[-1]
                    current_eq.add_digit(deep_result)

            if current_eq.is_complete:
                interim = current_eq.resolve()
                logging.debug(
                    "[%s] Calculation was complete = %s", len(calculation), interim
                )
            logging.debug("[%s] Resulting calcs: %s", len(calculation), calculation)

        #  Resolve pending at the end
        while len(calculation) > 1:
            deep_result = calculation.pop().left
            current_eq = calculation[-1]
            current_eq.add_digit(deep_result)
            current_eq.resolve()

        logging.debug("[%s] ### Final equation: %s", len(calculation), current_eq)
        return current_eq.left


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=18)
    homework = puzzle.input_data.strip().splitlines()
    puzzle.answer_a = sum([Calculator(equation).result for equation in homework])
    puzzle.answer_b = sum(
        [Calculator(equation).advanced_result for equation in homework]
    )
