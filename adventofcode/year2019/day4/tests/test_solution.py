import pytest

from adventofcode.year2019.day4.solution import DepotPassword, count_valid_passwords


@pytest.mark.parametrize(
    "pw,is_valid,has_double,does_not_decrease,digits,part_b_rules",
    [
        ("123456", False, False, True, [1, 2, 3, 4, 5, 6], False),
        ("113456", True, True, True, [1, 1, 3, 4, 5, 6], False),
        ("113450", False, True, False, [1, 1, 3, 4, 5, 0], False),
        ("112233", True, True, True, [1, 1, 2, 2, 3, 3], True),
        ("123444", False, False, True, [1, 2, 3, 4, 4, 4], True),
        ("111122", True, True, True, [1, 1, 1, 1, 2, 2], True),
    ],
)
def test_depot_password(
    pw, is_valid, has_double, does_not_decrease, digits, part_b_rules
):
    pw = DepotPassword(pw)
    assert pw.is_valid(part_b_rules) == is_valid
    assert pw.has_double(part_b_rules) == has_double
    assert pw.does_not_decrease() == does_not_decrease
    assert pw.digits == digits


@pytest.mark.parametrize("part_b_rules, expected", [(True, 0), (False, 4)])
def test_count_valid_passwords(part_b_rules, expected):
    assert count_valid_passwords(111110, 111114, part_b_rules) == expected
