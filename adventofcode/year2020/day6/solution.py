from aocd.models import Puzzle


class CustomsForm:
    def __init__(self, line):
        self.line = line
        self.answers = set(line)


class CustomsGroup:
    def __init__(self, group):
        self.group = group
        self.forms = [CustomsForm(line) for line in group.split("\n")]

    @property
    def yeses(self):
        yeses = set()
        for form in self.forms:
            yeses.update(form.answers)
        return yeses


class CustomsCollection:
    def __init__(self, collection_data):
        self.groups = [
            CustomsGroup(group_data) for group_data in collection_data.split("\n\n")
        ]

    @property
    def sum_of_yeses(self):
        return sum([len(g.yeses) for g in self.groups])


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=6)
    cc = CustomsCollection(puzzle.input_data)
    puzzle.answer_a = cc.sum_of_yeses
