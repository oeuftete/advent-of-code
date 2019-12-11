#!/usr/bin/env python

from aocd.models import Puzzle

from adventofcode.year2019.day10.solution import AsteroidMap

if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=10)
    a_map = AsteroidMap(puzzle.input_data)
    puzzle.answer_a = a_map.best_asteroid.n_viewable

    a_map.run_vaporizer()
    vaporized_asteroid = a_map.vaporized[199]
    puzzle.answer_b = 100 * vaporized_asteroid.x + vaporized_asteroid.y
