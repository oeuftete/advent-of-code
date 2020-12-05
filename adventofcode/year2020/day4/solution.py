import logging
import re
from functools import partial

from aocd.models import Puzzle

logging.basicConfig(level=logging.INFO)


class PassportBatch:
    def __init__(self, raw):
        self.raw = raw
        self.passports = []
        self._build_passports()

    def _build_passports(self):
        """Parse an entire batch into a list of passport fields."""
        for raw_p in self.raw.split("\n\n"):
            passport_fields = {}
            for p_field in raw_p.split():
                k, v = p_field.split(":", maxsplit=1)
                passport_fields[k] = v
            self.passports.append(Passport(passport_fields))

    def valid_passports(self, allow_missing_fields=None, strict=False):
        allow_missing_fields = allow_missing_fields or []
        return list(
            filter(
                lambda p: p.is_valid(
                    allow_missing_fields=allow_missing_fields, strict=strict
                ),
                self.passports,
            )
        )


class Passport:
    FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]

    def height_validator(hgt):
        m = re.fullmatch(r"(\d{2,3})(cm|in)", hgt)
        if not m:
            return False

        scalar, units = m.groups()
        scalar = int(scalar)

        if units == "cm":
            if scalar < 150 or scalar > 193:
                return False
        elif units == "in":
            if scalar < 59 or scalar > 76:
                return False
        else:  # bad units
            return False

        return True

    def year_validator(year, low, high):
        return (
            len(year) == 4 and year.isdigit() and int(year) >= low and int(year) <= high
        )

    STRICT_VALIDATORS = {
        "byr": partial(year_validator, low=1920, high=2002),
        "iyr": partial(year_validator, low=2010, high=2020),
        "eyr": partial(year_validator, low=2020, high=2030),
        "hgt": height_validator,
        "hcl": lambda s: bool(re.fullmatch(r"#[0-9a-f]{6}", s)),
        "ecl": lambda s: s in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
        "pid": lambda s: len(s) == 9 and s.isdigit(),
        "cid": lambda s: True,
    }

    def __init__(self, raw):
        for k in raw:
            if k in self.FIELDS:
                setattr(self, k, raw[k])
            else:
                raise ValueError(f"Unexpected field [{k}]")

    def is_valid(self, allow_missing_fields=None, strict=False):
        allow_missing_fields = allow_missing_fields or []

        for f in self.FIELDS:
            fv = getattr(self, f, None)
            if not fv and f not in allow_missing_fields:
                logging.debug("Missing attribute %s", f)
                return False
            if strict:
                if not self.STRICT_VALIDATORS[f](fv):
                    logging.debug("Strict validation failed: %s=%s", f, fv)
                    return False

        return True


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=4)
    batch = puzzle.input_data
    puzzle.answer_a = len(
        PassportBatch(batch).valid_passports(allow_missing_fields=["cid"])
    )
    puzzle.answer_b = len(
        PassportBatch(batch).valid_passports(allow_missing_fields=["cid"], strict=True)
    )
