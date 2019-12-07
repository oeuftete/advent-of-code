#!/usr/bin/env python

from aocd.models import Puzzle

from adventofcode.year2019.day7.solution import AmplificationMaximizer

if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=7)

    am = AmplificationMaximizer(puzzle.input_data)
    puzzle.answer_a = am.max_output_signal

    am_feedback = AmplificationMaximizer(puzzle.input_data, feedback=True)
    puzzle.answer_b = am_feedback.max_output_signal
