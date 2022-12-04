from enum import Enum

import attr
from aocd.models import Puzzle
from cached_property import cached_property


class RPS(Enum):
    ROCK = A = X = 1
    PAPER = B = Y = 2
    SCISSORS = C = Z = 3


@attr.s
class Game:
    p1: RPS = attr.ib()
    p2: RPS = attr.ib()

    @cached_property
    def result(self) -> int:
        p1 = self.p1
        p2 = self.p2
        if p1 == p2:
            return 0

        # pylint: disable=too-many-boolean-expressions
        if (
            (p1 == RPS.ROCK and p2 == RPS.SCISSORS)
            or (p1 == RPS.PAPER and p2 == RPS.ROCK)
            or (p1 == RPS.SCISSORS and p2 == RPS.PAPER)
        ):
            return 1
        return -1


@attr.s
class StrategyGuide:
    guide_text: str = attr.ib()
    game_scores: list[int] = attr.ib(factory=list, init=False)

    def __attrs_post_init__(self) -> None:
        for game in self.guide_text.splitlines():
            (p_them, p_me) = game.split()
            rps_them = RPS[p_them]
            rps_me = RPS[p_me]
            self.game_scores.append(
                3 * (Game(rps_me, rps_them).result + 1) + rps_me.value
            )

    @cached_property
    def total_score(self) -> int:
        return sum(self.game_scores)


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=2)
    strategy_guide = StrategyGuide(puzzle.input_data.strip())
    puzzle.answer_a = strategy_guide.total_score
