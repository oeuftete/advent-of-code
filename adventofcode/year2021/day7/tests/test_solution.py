import pytest

from adventofcode.year2021.day7.solution import CrabAligner


@pytest.fixture(name="example_positions")
def fixture_example_positions():
    return "16,1,2,0,4,2,7,1,2,14".split(",")


def test_example_positions(example_positions):
    aligner = CrabAligner(example_positions)
    assert len(aligner.positions) == 10
    assert aligner.positions[0] == 16

    assert aligner.alignment_fuel_expenditure == 37

    aligner = CrabAligner(example_positions, is_escalating_fuel_cost=True)
    assert aligner.alignment_fuel_expenditure == 168
