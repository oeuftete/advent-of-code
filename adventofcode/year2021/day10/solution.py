import logging

import attr
from aocd.models import Puzzle  # type: ignore

LOGGER = logging.getLogger("solveaocd")


@attr.s
class ParserLine:
    line: str = attr.ib()
    is_corrupt: bool = attr.ib(init=False, default=False)
    first_illegal: str = attr.ib(init=False, default="")
    is_incomplete: bool = attr.ib(init=False, default=False)
    autocompletion: str = attr.ib(init=False, default="")

    def __attrs_post_init__(self):
        PAIR_MAP = {}
        for k, v in {
            ")": "(",
            "]": "[",
            "}": "{",
            ">": "<",
        }.items():
            PAIR_MAP[k] = v
            PAIR_MAP[v] = k

        stack = []
        for c in self.line:
            if c in "([{<":
                stack.append(c)
            if c in ")]}>":
                if stack[-1] == PAIR_MAP[c]:
                    stack.pop()
                else:
                    self.first_illegal = c
                    self.is_corrupt = True
                    return

        if not stack:
            return

        self.is_incomplete = True
        while stack:
            self.autocompletion += PAIR_MAP[stack.pop()]


@attr.s
class Parser:
    lines: list[str] = attr.ib()
    parsed_lines: list[ParserLine] = attr.ib(init=False, factory=list)
    syntax_score: int = attr.ib(init=False, default=0)

    def __attrs_post_init__(self):
        self.parsed_lines = list(map(ParserLine, self.lines))
        for l in self.parsed_lines:
            match (l.first_illegal):
                case ")":
                    self.syntax_score += 3
                case "]":
                    self.syntax_score += 57
                case "}":
                    self.syntax_score += 1197
                case ">":
                    self.syntax_score += 25137

    @property
    def corrupt_lines(self) -> list[ParserLine]:
        return list(filter(lambda l: l.is_corrupt, self.parsed_lines))

    @property
    def incomplete_lines(self) -> list[ParserLine]:
        return list(filter(lambda l: l.is_incomplete, self.parsed_lines))

    @staticmethod
    def autocomplete_score(s: str) -> int:
        score = 0
        for c in s:
            match (c):
                case ")":
                    score = 5 * score + 1
                case "]":
                    score = 5 * score + 2
                case "}":
                    score = 5 * score + 3
                case ">":
                    score = 5 * score + 4

            LOGGER.debug("Interim score for -%s-: %d", s, score)
        return score

    @property
    def middle_score(self) -> int:
        completion_scores = list(
            map(
                lambda l: self.autocomplete_score(l.autocompletion),
                self.incomplete_lines,
            )
        )
        LOGGER.debug(completion_scores)
        return sorted(completion_scores)[len(completion_scores) // 2]


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=10)
    lines = puzzle.input_data.strip().splitlines()
    puzzle.answer_a = Parser(lines).syntax_score
    puzzle.answer_b = Parser(lines).middle_score
