import pytest

from adventofcode.year2019.day7.solution import AmplificationMaximizer


@pytest.mark.parametrize("opcodes,max_phase_sequence,max_output_signal", [
    ("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", (4, 3, 2, 1, 0), 43210),
    ("3,23,3,24,1002,24,10,24,1002,23,-1,23,"
     "101,5,23,23,1,24,23,23,4,23,99,0,0", (0, 1, 2, 3, 4), 54321),
    ("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,"
     "1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0",
     (1, 0, 4, 3, 2), 65210),
])
def test_max_output_signal(opcodes, max_phase_sequence, max_output_signal):
    am = AmplificationMaximizer(opcodes)
    assert am.max_output_signal == max_output_signal
    assert am.max_phase_sequence == max_phase_sequence
