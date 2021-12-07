import itertools
import logging
from collections import defaultdict

import attr
from aocd.models import Puzzle  # type: ignore

logging.basicConfig(level=logging.INFO)


@attr.s
class BingoBoardValue:
    value: int = attr.ib()
    marked: bool = attr.ib(default=False)

    def mark(self) -> None:
        self.marked = True


@attr.s
class BingoBoard:
    board_data: list[str] = attr.ib()
    board: dict[int, dict[int, BingoBoardValue]] = attr.ib(
        init=False, factory=lambda: defaultdict(dict)
    )
    board_index: dict = attr.ib(init=False, factory=dict)

    def __attrs_post_init__(self) -> None:
        for i, row in enumerate(self.board_data):
            for j, board_value in enumerate(list(map(int, row.strip().split()))):
                self.board[i][j] = BingoBoardValue(value=board_value)
                self.board_index[board_value] = (i, j)
                logging.debug("Set [%s][%s] to [%s]", i, j, board_value)

    def mark(self, value) -> None:
        """Look for the given value and mark it if found."""
        if value in self.board_index:
            i, j = self.board_index[value]
            logging.debug(
                "Marking value [%s] at [%s, %s]: (%s)", value, i, j, self.board[i][j]
            )
            self.board[i][j].mark()

    @property
    def is_complete(self) -> bool:
        for i in self.board:
            if all(map(lambda v: v.marked, self.board[i].values())):
                logging.debug("Found bingo: row [%s]: %s", i, self.board[i])
                return True

        for j in range(5):
            if all(
                map(
                    lambda v: v.marked,
                    map(
                        lambda i, j=j: self.board[i][j], range(5)  # type: ignore[misc]
                    ),
                )
            ):
                logging.debug("Found bingo: column [%s]", j)
                return True

        logging.debug("No bingo.")
        return False

    @property
    def sum_unmarked(self) -> int:
        sum_unmarked = 0
        for i in self.board:
            for v in self.board[i].values():
                if not v.marked:
                    sum_unmarked += v.value
        return sum_unmarked


@attr.s
class BingoBoardSet:
    bingo_data: list[str] = attr.ib()
    find_last: bool = attr.ib(default=False)
    draws: list[int] = attr.ib(init=False)
    boards: list[BingoBoard] = attr.ib(init=False, factory=list)
    last_drawn: int = attr.ib(init=False)
    winning_board: BingoBoard = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
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

            for b in filter(lambda board: not board.is_complete, self.boards):
                logging.debug("Now marking: %s on %s", d, b)
                b.mark(d)
                if b.is_complete:
                    logging.debug("WINNER! %s", b)
                    if self.find_last:
                        if all(map(lambda board: board.is_complete, self.boards)):
                            self.winning_board = b
                            return
                    else:
                        self.winning_board = b
                        return

        raise ValueError("No winner found!")

    @property
    def final_score(self) -> int:
        return self.winning_board.sum_unmarked * self.last_drawn


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=4)
    bingo_data = puzzle.input_data.strip().splitlines()
    puzzle.answer_a = BingoBoardSet(bingo_data).final_score
    puzzle.answer_b = BingoBoardSet(bingo_data, find_last=True).final_score
