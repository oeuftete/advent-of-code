import pytest

from adventofcode.year2020.day18.solution import Calculator


@pytest.mark.parametrize(
    "equation,result,advanced_result",
    [
        ("1 + 2 * 3 + 4 * 5 + 6", 71, 231),
        ("1 + (2 * 3) + (4 * (5 + 6))", 51, 51),
        ("2 * 3 + (4 * 5)", 26, 46),
        ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437, 1445),
        ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240, 669060),
        ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632, 23340),
    ],
)
def test_calculator(equation, result, advanced_result):
    assert Calculator(equation).result == result
    assert Calculator(equation).advanced_result == advanced_result
