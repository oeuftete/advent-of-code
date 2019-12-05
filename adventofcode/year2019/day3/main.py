#!/usr/bin/env python

from aocd.models import Puzzle
from adventofcode.year2019.day3.solution import closest_intersection

if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=3)
    (path_one, path_two) = puzzle.input_data.split('\n')
    puzzle.answer_a = closest_intersection(path_one, path_two)
    puzzle.answer_b = closest_intersection(path_one, path_two, use_steps=True)
