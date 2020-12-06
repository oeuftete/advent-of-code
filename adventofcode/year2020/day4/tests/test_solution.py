import pytest

from adventofcode.year2020.day4.solution import Passport, PassportBatch


@pytest.fixture(name="batch")
def fixture_batch():
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


@pytest.fixture(name="invalid_batch")
def fixture_invalid_batch():
    return """
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""


@pytest.fixture(name="valid_batch")
def fixture_valid_batch():
    return """
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""


def test_passport():
    with pytest.raises(ValueError):
        Passport({"foo": "bar"})


@pytest.mark.parametrize(
    "field,value,is_valid",
    [
        ("byr", "2002", True),
        ("byr", "2003", False),
        ("hgt", "60in", True),
        ("hgt", "150cm", True),
        ("hgt", "190cm", True),
        ("hgt", "190in", False),
        ("hgt", "190", False),
        ("hcl", "#123abc", True),
        ("hcl", "#123abz", False),
        ("hcl", "123abc", False),
        ("ecl", "brn", True),
        ("ecl", "wat", False),
        ("pid", "000000001", True),
        ("pid", "0123456789", False),
    ],
)
def test_strict_rules(field, value, is_valid):
    assert Passport.strict_validators()[field](value) == is_valid


def test_passport_batch(batch):
    pb = PassportBatch(batch)
    assert len(pb.passports) == 4
    assert pb.passports[0].ecl == "gry"
    assert pb.passports[2].ecl == "brn"

    assert len(pb.valid_passports()) == 1
    assert len(pb.valid_passports(allow_missing_fields=["cid"])) == 2


def test_strict_invalid_batch(invalid_batch):
    pb = PassportBatch(invalid_batch)
    assert len(pb.passports) == 4
    assert len(pb.valid_passports(allow_missing_fields=["cid"], strict=True)) == 0


def test_strict_valid_batch(valid_batch):
    pb = PassportBatch(valid_batch)
    assert len(pb.passports) == 4
    assert len(pb.valid_passports(allow_missing_fields=["cid"], strict=True)) == 4
