#!/usr/bin/env python

from aocd.models import Puzzle

from adventofcode.year2019.day13.solution import ArcadeCabinet

if __name__ == "__main__":
    puzzle = Puzzle(year=2019, day=13)

    game = ArcadeCabinet(puzzle.input_data)
    puzzle.answer_a = game.blocks_count

    play = ArcadeCabinet(puzzle.input_data, play=True, manual=False, screen=False)
    puzzle.answer_b = play.score
