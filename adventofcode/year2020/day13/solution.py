import itertools
import math
from dataclasses import dataclass, field

from aocd.models import Puzzle


@dataclass
class BusNotes:
    raw_notes: str
    timestamp: int = 0
    bus_ids: list = field(default_factory=list)

    def __post_init__(self):
        if self.raw_notes:
            lines = self.raw_notes.strip().splitlines()
            self.timestamp = int(lines.pop(0))
            self.bus_ids = [int(n) for n in lines.pop(0).split(",") if n != "x"]

    @property
    def waiting_product(self):
        for t in itertools.count(start=self.timestamp):
            for bus_id in self.bus_ids:
                if t % bus_id == 0:
                    return (t - self.timestamp) * bus_id

        return math.inf


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=13)
    bus_notes = BusNotes(puzzle.input_data)
    puzzle.answer_a = bus_notes.waiting_product
