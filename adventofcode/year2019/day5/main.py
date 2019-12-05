#!/usr/bin/env python

from aocd.models import Puzzle

from adventofcode.common.year2019.intcode_computer import Intcode

if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=5)

    intcode_a = Intcode(puzzle.input_data, input_data=[1])
    intcode_a.execute()
    puzzle.answer_a = intcode_a.output_data[-1]

    intcode_b = Intcode(puzzle.input_data, input_data=[5])
    intcode_b.execute()
    puzzle.answer_b = intcode_b.output_data[-1]
