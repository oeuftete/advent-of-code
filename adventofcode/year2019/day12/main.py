#!/usr/bin/env python

from aocd.models import Puzzle

from adventofcode.year2019.day12.solution import LunarOrrery

if __name__ == "__main__":
    puzzle = Puzzle(year=2019, day=12)
    orrery = LunarOrrery(puzzle.input_data)
    orrery.iterate(1000)
    puzzle.answer_a = orrery.total_energy

    #  Much too slow!
    #
    #  orrery.iterate_until_equal()
    #  puzzle.answer_b = orrery.iterations
