import pytest
from bitarray.util import ba2int

from adventofcode.year2020.day14.solution import SeaportComputer


@pytest.fixture(name="simple_program")
def fixture_simple_program():
    return """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""".strip().splitlines()


@pytest.fixture(name="v2_program")
def fixture_v2_program():
    return """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
""".strip().splitlines()


def test_simple_program(simple_program):
    computer = SeaportComputer(simple_program)
    computer.process()

    assert ba2int(computer.memory[7]) == 101
    assert ba2int(computer.memory[8]) == 64
    assert ba2int(computer.memory[9]) == 0
    assert computer.sum_memory() == 165


def test_v2_program(v2_program):
    computer = SeaportComputer(v2_program, version=2)
    computer.process()

    assert computer.sum_memory() == 208
