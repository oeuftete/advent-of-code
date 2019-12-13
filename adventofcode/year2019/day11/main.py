#!/usr/bin/env python

from aocd.models import Puzzle

from adventofcode.year2019.day11.solution import PaintingRun

if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=11)
    run = PaintingRun(puzzle.input_data)
    run.execute()
    puzzle.answer_a = run.unique_painted_panels
