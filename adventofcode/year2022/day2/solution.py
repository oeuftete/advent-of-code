from enum import IntEnum
from functools import cached_property

import attr
from aocd.models import Puzzle


class RPS(IntEnum):
    ROCK = A = X = 1
    PAPER = B = Y = 2
    SCISSORS = C = Z = 3


class RpsResult(IntEnum):
    X = LOSS = -1
    Y = DRAW = 0
    Z = WIN = 1


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
    real_scoring: bool = attr.ib(default=False)
    game_scores: list[int] = attr.ib(factory=list, init=False)

    def game_score(self, rps_result: RpsResult, rps_me: RPS) -> int:
        return 3 * (rps_result + 1) + rps_me

    def _generate_real_scores(self):
        for game in self.guide_text.splitlines():
            (p_them, required_result) = game.split()
            rps_them = RPS[p_them]
            rps_required_result = RpsResult[required_result]

            rps_required_me = (rps_them + rps_required_result) % 3
            if rps_required_me == 0:
                rps_required_me = 3

            self.game_scores.append(
                self.game_score(rps_required_result, rps_required_me)
            )

    def _generate_naive_scores(self):
        for game in self.guide_text.splitlines():
            (p_them, p_me) = game.split()
            rps_them = RPS[p_them]
            rps_me = RPS[p_me]
            self.game_scores.append(
                self.game_score(Game(rps_me, rps_them).result, rps_me)
            )

    def generate_scores(self):
        self.game_scores = []
        if self.real_scoring:
            self._generate_real_scores()
        else:
            self._generate_naive_scores()

    @property
    def total_score(self) -> int:
        return sum(self.game_scores)


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=2)

    strategy_guide = StrategyGuide(puzzle.input_data.strip())
    strategy_guide.generate_scores()
    puzzle.answer_a = strategy_guide.total_score

    strategy_guide.real_scoring = True
    strategy_guide.generate_scores()
    puzzle.answer_b = strategy_guide.total_score
