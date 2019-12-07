#!/usr/bin/env python

from aocd.models import Puzzle

from adventofcode.common.year2019.intcode_computer import Intcode
from adventofcode.year2019.day2.solution import find_inputs

if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=2)
    opcodes = puzzle.input_data

    intcode = Intcode(opcodes, noun=12, verb=2)
    intcode.execute()
    puzzle.answer_a = intcode.opcodes[0]

    b_tuple = find_inputs(opcodes, 19690720)
    puzzle.answer_b = 100 * b_tuple[0] + b_tuple[1]
