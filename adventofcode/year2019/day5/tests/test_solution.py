from aocd.models import Puzzle

from adventofcode.common.year2019.intcode_computer import Intcode


def test_day5_solution():
    """Verify my submitted correct solution continues to work."""
    puzzle = Puzzle(year=2019, day=5)
    intcode = Intcode(puzzle.input_data, input_data=[1])
    intcode.execute()
    assert intcode.output_data[-1] == int(puzzle.answer_a)
