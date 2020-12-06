from dataclasses import dataclass

from aocd.models import Puzzle


@dataclass
class CustomsForm:
    line: str

    @property
    def answers(self) -> set:
        return set(self.line)


class CustomsGroup:
    def __init__(self, group):
        self.group = group
        self.forms = [CustomsForm(line) for line in group.split("\n")]

    @property
    def any_yeses(self):
        any_yeses = set()
        for form in self.forms:
            any_yeses.update(form.answers)
        return any_yeses

    @property
    def all_yeses(self):
        all_yeses = None
        for form in self.forms:
            if all_yeses is None:
                all_yeses = form.answers
            else:
                all_yeses.intersection_update(form.answers)
        return all_yeses


class CustomsCollection:
    def __init__(self, collection_data):
        self.groups = [
            CustomsGroup(group_data) for group_data in collection_data.split("\n\n")
        ]

    @property
    def sum_of_any_yeses(self):
        return sum([len(g.any_yeses) for g in self.groups])

    @property
    def sum_of_all_yeses(self):
        return sum([len(g.all_yeses) for g in self.groups])


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=6)
    cc = CustomsCollection(puzzle.input_data)
    puzzle.answer_a = cc.sum_of_any_yeses
    puzzle.answer_b = cc.sum_of_all_yeses
