import itertools
import logging
import typing
from collections import defaultdict

import attr
from aocd.models import Puzzle

logging.basicConfig(level=logging.INFO)


@attr.s
class BingoBoardValue:
    value: int = attr.ib()
    marked: bool = attr.ib(default=False)

    def mark(self):
        self.marked = True


@attr.s
class BingoBoard:
    board_data: typing.List[str] = attr.ib()
    board: typing.Dict = attr.ib(init=False, factory=lambda: defaultdict(dict))
    board_index: typing.Dict = attr.ib(init=False, factory=dict)

    def __attrs_post_init__(self):
        for i, row in enumerate(self.board_data):
            for j, board_value in enumerate(list(map(int, row.strip().split()))):
                self.board[i][j] = BingoBoardValue(value=board_value)
                self.board_index[board_value] = (i, j)
                logging.debug("Set [%s][%s] to [%s]", i, j, board_value)

    def mark(self, value):
        """Look for the given value and mark it if found."""
        if value in self.board_index:
            i, j = self.board_index[value]
            logging.debug(
                "Marking value [%s] at [%s, %s]: (%s)", value, i, j, self.board[i][j]
            )
            self.board[i][j].mark()

    @property
    def is_complete(self):
        for i in self.board:
            if all(map(lambda v: v.marked, self.board[i].values())):
                logging.debug("Found bingo: row [%s]: %s", i, self.board[i])
                return True

        for j in range(4):
            if all(
                map(lambda v: v.marked, map(lambda i, j=j: self.board[i][j], range(4)))
            ):
                logging.debug("Found bingo: column [%s]", j)
                return True

        return False

    @property
    def sum_unmarked(self):
        sum_unmarked = 0
        for i in self.board:
            for v in self.board[i].values():
                if not v.marked:
                    sum_unmarked += v.value
        return sum_unmarked


@attr.s
class BingoBoardSet:
    bingo_data: typing.List[str] = attr.ib()
    draws: typing.List[int] = attr.ib(init=False)
    boards: typing.List[BingoBoard] = attr.ib(init=False, factory=list)
    last_drawn: int = attr.ib(init=False)
    winning_board: BingoBoard = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.draws = list(map(int, self.bingo_data[0].split(",")))

        #  Starting from line 2, grab the board's rows
        for i in itertools.count(start=2, step=6):
            if i > len(self.bingo_data):
                break
            logging.debug("Appending board from line %s in input", i)
            self.boards.append(BingoBoard(self.bingo_data[i : i + 5]))

        # Play the game
        for d in self.draws:
            logging.debug("Now drawing: %s", d)
            self.last_drawn = d
            for b in self.boards:
                logging.debug("Now marking: %s on %s", d, b)
                b.mark(d)
                if b.is_complete:
                    logging.debug("WINNER! %s", b)
                    self.winning_board = b
                    return

        raise ValueError("No winner found!")

    @property
    def final_score(self):
        return self.winning_board.sum_unmarked * self.last_drawn


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=4)
    bingo_data = puzzle.input_data.strip().splitlines()
    puzzle.answer_a = BingoBoardSet(bingo_data).final_score
