#!/usr/bin/env python

from aocd.models import Puzzle

from adventofcode.common.year2019.intcode_computer import Intcode

if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=9)
    opcodes = puzzle.input_data

    intcode = Intcode(opcodes, input_data=[1])
    intcode.execute()
    puzzle.answer_a = intcode.last_output
