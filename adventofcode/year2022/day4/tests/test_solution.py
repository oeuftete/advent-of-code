import pytest

from adventofcode.year2022.day4.solution import AssignmentValidator


@pytest.fixture(name="example_assignments")
def fixture_example_assignments():
    return """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""".strip().splitlines()


def test_example_assignments(example_assignments):
    assignment_validator = AssignmentValidator(example_assignments)
    assert assignment_validator.n_pairs_contained == 2
    assert assignment_validator.n_pairs_overlap == 4
