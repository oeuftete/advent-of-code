import pytest

from adventofcode.year2020.day8.solution import ConsoleComputer


@pytest.fixture(name="boot_code")
def fixture_boot_code():
    return """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
""".strip()


def test_boot_code(boot_code):
    computer = ConsoleComputer(boot_code)
    computer.run_until_loop()
    assert computer.accumulator == 5

    computer.reset()
    assert computer.run_with_toggles_accumulator == 8
