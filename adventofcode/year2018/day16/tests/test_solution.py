import pytest

from adventofcode.year2018.day16.solution import Cpu, CpuMonitor

SAMPLE_DATA = """
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]



1 2 3 4
0 1 2 3
""".strip().split(
    "\n"
)


@pytest.mark.parametrize(
    "opcode,before,operation,after",
    [
        ("ADDR", [3, 2, 1, 1], [0, 1, 1, 2], [3, 2, 4, 1]),
        ("ADDI", [3, 2, 1, 1], [0, 1, 1, 2], [3, 2, 3, 1]),
    ],
)
def test_op_codes(opcode, before, operation, after):
    c = Cpu(before)
    c.op(opcode, *operation[1:])
    assert c.registers == after


def test_cpu_monitor():
    monitor = CpuMonitor(SAMPLE_DATA)
    assert len(monitor.samples) == 1
    assert monitor.data == [[1, 2, 3, 4], [0, 1, 2, 3]]

    s0 = monitor.samples[0]
    assert s0.before == [3, 2, 1, 1]
    assert s0.operation == [9, 2, 1, 2]
    assert s0.after == [3, 2, 2, 1]

    assert len(s0.possible_opcodes) == 3
    assert monitor.find_ambiguous(3) == 1

    assert monitor.possible_opcode_matches == {9: set(["MULR", "ADDI", "SETI"])}
