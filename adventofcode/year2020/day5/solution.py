from aocd.models import Puzzle


class Manifest:
    def __init__(self, passes):
        self.passes = passes

    @property
    def max_seat_id(self):
        return max(map(lambda p: p.seat_id, self.passes))

    @property
    def empty_seat(self):
        seat_ids = [p.seat_id for p in self.passes]
        for seat_id in range(min(seat_ids), max(seat_ids)):
            if seat_id not in seat_ids:
                return seat_id


class BoardingPass:
    def __init__(self, code):
        self.code = code

    @property
    def seat_id(self):
        return int(
            self.code.replace("F", "0")
            .replace("B", "1")
            .replace("L", "0")
            .replace("R", "1"),
            2,
        )


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=5)
    manifest = Manifest([BoardingPass(code) for code in puzzle.input_data.split("\n")])
    puzzle.answer_a = manifest.max_seat_id
    puzzle.answer_b = manifest.empty_seat
