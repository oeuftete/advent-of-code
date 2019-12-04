from aocd.models import Puzzle
import pytest

from adventofcode.year2019.day2.solution import (find_inputs, run_program)


@pytest.mark.parametrize("opcodes,output_codes", [
    ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
    ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
    ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
])
def test_run_program(opcodes, output_codes):
    assert run_program(opcodes) == output_codes


@pytest.mark.parametrize("opcodes,output_0,noun,verb", [
    ([int(op) for op in Puzzle(year=2019, day=2).input_data.split(',')
      ], 3765464, 12, 2),
])
def test_find_inputs(opcodes, output_0, noun, verb):
    assert find_inputs(opcodes, output_0) == (noun, verb)


@pytest.mark.parametrize("opcodes", [
    [3, 0, 0, 0, 99],
    [1, 1, 1, 4, 99, 5, 6, 0, 0],
])
def test_run_program_bad_op(opcodes):
    with pytest.raises(Exception) as e:
        assert 'Unknown opcode' in str(e.value)


@pytest.mark.parametrize("opcodes", [
    [],
    [3, 0, 0, 0],
    [1, 1, 1, 4, 99, 5, 6, 0],
])
def test_run_program_early_exit(opcodes):
    with pytest.raises(Exception) as e:
        assert 'Unterminated program' in str(e.value)
