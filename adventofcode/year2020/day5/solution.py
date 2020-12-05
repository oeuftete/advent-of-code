from aocd.models import Puzzle


class Manifest:
    def __init__(self, passes):
        self.passes = passes

    @property
    def max_seat_id(self):
        return max(map(lambda p: p.seat_id, self.passes))


class BoardingPass:
    def __init__(self, code):
        self.code = code
        self.row = code[:7]
        self.column = code[7:]

    @property
    def row_number(self):
        return int(self.row.replace("F", "0").replace("B", "1"), 2)

    @property
    def column_number(self):
        return int(self.column.replace("L", "0").replace("R", "1"), 2)

    @property
    def seat_id(self):
        return self.row_number * 8 + self.column_number


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=5)
    manifest = Manifest([BoardingPass(code) for code in puzzle.input_data.split("\n")])
    puzzle.answer_a = manifest.max_seat_id
    #  puzzle.answer_b = ExpenseReport(expenses, tuple_size=3).product_2020
