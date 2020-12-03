import pytest

from adventofcode.year2020.day2.solution import PasswordRule, PasswordValidator


@pytest.fixture
def password_list():
    return """
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
""".strip().split(
        "\n"
    )


def test_password_rule():
    raw = "1-3 a"
    rule = PasswordRule(raw)
    assert 0 not in rule.count_range
    assert 1 in rule.count_range
    assert 3 in rule.count_range
    assert 4 not in rule.count_range
    assert rule.character == "a"

    assert rule.validate_password("abcde") == True
    assert rule.validate_password("abada") == True
    assert rule.validate_password("fghij") == False
    assert rule.validate_password("aaaaa") == False


def test_password_rule_new():
    raw = "1-3 a"
    rule = PasswordRule(raw, new_policy=True)
    assert 0 in rule.positions
    assert 1 not in rule.positions
    assert 2 in rule.positions
    assert 3 not in rule.positions
    assert rule.character == "a"

    assert rule.validate_password("abcde") == True
    assert rule.validate_password("abada") == False
    assert rule.validate_password("fghij") == False
    assert rule.validate_password("aaaaa") == False
    assert rule.validate_password("baaaa") == True


def test_password_validator(password_list):
    password_validator = PasswordValidator(password_list)
    valid = password_validator.valid_passwords
    assert len(valid) == 2
    assert "abcde" in valid
    assert "cdefg" not in valid
    assert "ccccccccc" in valid


def test_password_validator_new(password_list):
    password_validator = PasswordValidator(password_list, new_policy=True)
    valid = password_validator.valid_passwords
    assert len(valid) == 1
    assert "abcde" in valid
    assert "cdefg" not in valid
    assert "ccccccccc" not in valid
