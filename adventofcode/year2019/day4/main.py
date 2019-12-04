#!/usr/bin/env python

from aocd.models import Puzzle
from adventofcode.year2019.day4.solution import count_valid_passwords

if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=4)
    (low, high) = puzzle.input_data.split('-')

    puzzle.answer_a = count_valid_passwords(int(low), int(high))
    puzzle.answer_b = count_valid_passwords(int(low), int(high), True)
