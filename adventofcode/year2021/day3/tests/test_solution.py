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
    diag = Diagnostic(example_diagnostics)
    assert diag.power_consumption == 198
    assert diag.oxygen_rating == 23
    assert diag.scrubber_rating == 10
    assert diag.life_support_rating == 230
