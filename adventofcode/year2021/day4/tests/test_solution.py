import pytest

from adventofcode.year2021.day4.solution import BingoBoardSet


@pytest.fixture(name="example_set")
def fixture_example_set():
    return """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
""".strip().splitlines()


def test_bingo_board_set_day1(example_set):
    day1_set = BingoBoardSet(example_set)

    assert len(day1_set.boards) == 3
    assert day1_set.boards[1].board[2][2].value == 7
    assert day1_set.last_drawn == 24
    assert day1_set.winning_board.sum_unmarked == 188
    assert day1_set.final_score == 4512


def test_bingo_board_set_day2(example_set):
    day2_set = BingoBoardSet(example_set, find_last=True)
    assert day2_set.last_drawn == 13
    assert day2_set.winning_board.sum_unmarked == 148
    assert day2_set.final_score == 1924
