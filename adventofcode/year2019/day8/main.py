#!/usr/bin/env python

from aocd.models import Puzzle

from adventofcode.year2019.day8.solution import Image

if __name__ == "__main__":
    puzzle = Puzzle(year=2019, day=8)
    image = Image(puzzle.input_data, (25, 6))
    puzzle.answer_a = image.solution_a

    #  No auto-submission
    print(image.rendered_clearly)
