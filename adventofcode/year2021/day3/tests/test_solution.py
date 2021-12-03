import pytest

from adventofcode.year2021.day3.solution import Diagnostic


@pytest.fixture(name="example_diagnostics")
def fixture_example_course():
    return [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ]


def test_diagnostics(example_diagnostics):
    assert Diagnostic(example_diagnostics).gamma_rate == 22
    assert Diagnostic(example_diagnostics).epsilon_rate == 9
