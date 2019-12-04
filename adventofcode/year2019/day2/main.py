#!/usr/bin/env python

from aocd.models import Puzzle
from adventofcode.year2019.day2.solution import find_inputs, run_program

if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=2)
    opcodes = [int(op) for op in puzzle.input_data.split(',')]

    output_codes = run_program(opcodes.copy(), noun=12, verb=2)

    puzzle.answer_a = output_codes[0]
    b_tuple = find_inputs(opcodes, 19690720)
    puzzle.answer_b = 100 * b_tuple[0] + b_tuple[1]
