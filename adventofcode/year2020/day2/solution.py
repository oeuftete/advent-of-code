from dataclasses import dataclass

from aocd.models import Puzzle


@dataclass
class PasswordRule:
    raw_rule: str
    new_policy: bool = False

    def __post_init__(self):
        raw, character = self.raw_rule.split(" ")
        low, high = [int(r) for r in raw.split("-")]

        self.character = character
        if self.new_policy:
            self.positions = [low - 1, high - 1]
        else:
            self.count_range = range(low, high + 1)

    def validate_password(self, password):
        if self.new_policy:
            return (password[self.positions[0]] == self.character) != (
                password[self.positions[1]] == self.character
            )
        return password.count(self.character) in self.count_range


@dataclass
class PasswordValidator:
    password_list: list
    new_policy: bool = False

    @property
    def valid_passwords(self):
        valid = []
        for pw_line in self.password_list:
            (raw_rule, password) = pw_line.split(": ", maxsplit=1)
            rule = PasswordRule(raw_rule, self.new_policy)
            if rule.validate_password(password):
                valid.append(password)

        return valid


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=2)
    password_list = puzzle.input_data.split("\n")
    puzzle.answer_a = len(PasswordValidator(password_list).valid_passwords)
    puzzle.answer_b = len(
        PasswordValidator(password_list, new_policy=True).valid_passwords
    )
