import pytest

from adventofcode.year2017.day1.solution import Captcha


@pytest.mark.parametrize(
    "captcha,expected", [("1122", 3), ("1111", 4), ("1234", 0), ("91212129", 9)]
)
def test_captcha_solution(captcha, expected):
    assert Captcha(raw=captcha).solution == expected


@pytest.mark.parametrize(
    "captcha,expected",
    [("1212", 6), ("1221", 0), ("123425", 4), ("123123", 12), ("12131415", 4)],
)
def test_captcha_solution_two(captcha, expected):
    assert Captcha(raw=captcha).solution_two == expected
