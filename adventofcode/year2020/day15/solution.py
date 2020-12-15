import logging
from dataclasses import dataclass, field

from aocd.models import Puzzle

logging.basicConfig(level=logging.INFO)


@dataclass
class NumberGame:
    starting: list
    turn: int = field(init=False, default=0)
    spoken: int = field(init=False, default=0)
    record: dict = field(init=False, default_factory=dict)

    def take_turn(self, n=1):
        for _ in range(n):
            self.turn += 1
            last_spoken = self.spoken
            spoken = 0

            logging.debug(
                "[%s]: last=%s, record=%s", self.turn, last_spoken, self.record
            )

            #  record
            #    k: number
            #    v: (last_turn_spoken, next_to_last_turn_spoken)
            if self.starting:
                spoken = self.starting.pop(0)
                self.record[spoken] = (self.turn, -1)
            elif last_spoken in self.record:
                last_turn, next_to_last_turn = self.record[last_spoken]
                if next_to_last_turn == -1:
                    spoken = 0
                else:
                    spoken = last_turn - next_to_last_turn

                if spoken in self.record:
                    self.record[spoken] = (self.turn, self.record[spoken][0])
                else:
                    self.record[spoken] = (self.turn, -1)

            logging.debug("[%s]: spoken=%s", self.turn, spoken)

            self.spoken = spoken


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=15)
    starting = [int(m) for m in puzzle.input_data.splitlines()[0].split(",")]
    game = NumberGame(starting[:])
    game.take_turn(2020)

    puzzle.answer_a = game.spoken

    game = NumberGame(starting[:])
    game.take_turn(30000000)
    puzzle.answer_b = game.spoken
