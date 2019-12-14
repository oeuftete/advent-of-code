import pytest

from aocd.models import Puzzle

from adventofcode.year2019.day13.solution import ArcadeCabinet


@pytest.mark.slow
def test_day13_solution():
    """Verify my submitted correct solution continues to work."""
    puzzle = Puzzle(year=2019, day=13)

    game = ArcadeCabinet(puzzle.input_data)
    assert game.blocks_count == int(puzzle.answer_a)

    play = ArcadeCabinet(puzzle.input_data,
                         play=True,
                         manual=False,
                         screen=False)
    assert play.score == int(puzzle.answer_b)
