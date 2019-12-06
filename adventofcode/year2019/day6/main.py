#!/usr/bin/env python

from aocd.models import Puzzle

from adventofcode.year2019.day6.solution import OrbitMap

if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=6)
    o = OrbitMap(puzzle.input_data)
    puzzle.answer_a = o.n_all_orbits
    puzzle.answer_b = o.orbital_transfers('YOU', 'SAN')
