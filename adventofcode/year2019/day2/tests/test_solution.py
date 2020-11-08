from aocd.models import Puzzle
import pytest

from adventofcode.year2019.day2.solution import find_inputs


@pytest.mark.parametrize(
    "opcodes,output_0,noun,verb",
    [(Puzzle(year=2019, day=2).input_data, 3765464, 12, 2),],
)
def test_find_inputs(opcodes, output_0, noun, verb):
    assert find_inputs(opcodes, output_0) == (noun, verb)
