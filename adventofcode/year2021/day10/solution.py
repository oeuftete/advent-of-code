import attr
from aocd.models import Puzzle  # type: ignore


@attr.s
class ParserLine:
    line: str = attr.ib()
    is_corrupt: bool = attr.ib(init=False, default=False)
    first_illegal: str = attr.ib(init=False, default="")

    def __attrs_post_init__(self):
        OPENER_MAP = {
            ")": "(",
            "]": "[",
            "}": "{",
            ">": "<",
        }

        stack = []
        for c in self.line:
            if c in "([{<":
                stack.append(c)
            if c in ")]}>":
                if stack[-1] == OPENER_MAP[c]:
                    stack.pop()
                else:
                    self.first_illegal = c
                    self.is_corrupt = True

                    return


@attr.s
class Parser:
    lines: list[str] = attr.ib()
    parsed_lines: list[ParserLine] = attr.ib(init=False, factory=list)
    syntax_score: int = attr.ib(init=False, default=0)

    def __attrs_post_init__(self):
        self.parsed_lines = list(map(ParserLine, self.lines))
        for l in self.parsed_lines:
            match (l.first_illegal):
                case (")"):
                    self.syntax_score += 3
                case ("]"):
                    self.syntax_score += 57
                case ("}"):
                    self.syntax_score += 1197
                case (">"):
                    self.syntax_score += 25137

    @property
    def corrupt_lines(self) -> list[ParserLine]:
        return list(filter(lambda l: l.is_corrupt, self.parsed_lines))


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=10)
    lines = puzzle.input_data.strip().splitlines()
    puzzle.answer_a = Parser(lines).syntax_score
