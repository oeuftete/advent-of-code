#!/usr/bin/env python

from aocd.models import Puzzle

from adventofcode.year2019.day14.solution import Nanofactory

if __name__ == "__main__":
    puzzle = Puzzle(year=2019, day=14)
    factory = Nanofactory(puzzle.input_data)
    puzzle.answer_a = factory.minimum_ore
