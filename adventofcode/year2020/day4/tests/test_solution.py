import pytest

from adventofcode.year2020.day4.solution import Passport, PassportBatch


@pytest.fixture
def batch():
    return """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""


def test_passport():
    with pytest.raises(ValueError):
        Passport({"foo": "bar"})


def test_passport_batch(batch):
    pb = PassportBatch(batch)
    assert len(pb.passports) == 4
    assert pb.passports[0].ecl == "gry"
    assert pb.passports[2].ecl == "brn"

    assert len(pb.valid_passports()) == 1
    assert len(pb.valid_passports(["cid"])) == 2
