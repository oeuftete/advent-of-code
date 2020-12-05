import logging

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

    def valid_passports(self, allow_missing_fields=None):
        allow_missing_fields = allow_missing_fields or []
        return list(filter(lambda p: p.is_valid(allow_missing_fields), self.passports))


class Passport:
    FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]

    def __init__(self, raw):
        for k in raw:
            if k in self.FIELDS:
                setattr(self, k, raw[k])
            else:
                raise ValueError(f"Unexpected field [{k}]")

    def is_valid(self, allow_missing_fields=None):
        allow_missing_fields = allow_missing_fields or []
        for f in self.FIELDS:
            if not getattr(self, f, None) and f not in allow_missing_fields:
                logging.debug("Missing attribute {f}")
                return False

        return True


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=4)
    batch = puzzle.input_data
    puzzle.answer_a = len(PassportBatch(batch).valid_passports(["cid"]))
