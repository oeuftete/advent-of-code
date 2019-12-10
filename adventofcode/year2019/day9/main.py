#!/usr/bin/env python

from aocd.models import Puzzle

from adventofcode.common.year2019.intcode_computer import Intcode

if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=9)
    opcodes = puzzle.input_data

    intcode_test_mode = Intcode(opcodes, input_data=[1])
    intcode_test_mode.execute()
    puzzle.answer_a = intcode_test_mode.last_output

    intcode_boost_mode = Intcode(opcodes, input_data=[2])
    intcode_boost_mode.execute()
    puzzle.answer_b = intcode_boost_mode.last_output
