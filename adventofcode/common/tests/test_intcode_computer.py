import pytest

from adventofcode.common.year2019.intcode_computer import run_program


@pytest.mark.parametrize("opcodes,output_codes", [
    ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
    ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
    ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
])
def test_run_program(opcodes, output_codes):
    assert run_program(opcodes) == output_codes


@pytest.mark.parametrize("opcodes", [
    [3, 0, 0, 0, 99],
    [1, 1, 1, 4, 99, 5, 6, 0, 0],
])
def test_run_program_bad_op(opcodes):
    with pytest.raises(Exception) as e:
        run_program(opcodes)
        assert 'Unknown opcode' in str(e.value)


@pytest.mark.parametrize("opcodes", [
    [],
    [3, 0, 0, 0],
    [1, 1, 1, 4, 99, 5, 6, 0],
])
def test_run_program_early_exit(opcodes):
    with pytest.raises(Exception) as e:
        run_program(opcodes)
        assert 'Unterminated program' in str(e.value)
