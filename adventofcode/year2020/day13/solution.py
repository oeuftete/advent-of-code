import itertools
import logging
import math
from dataclasses import dataclass, field
from functools import partial

from aocd.models import Puzzle

logging.basicConfig(level=logging.INFO)


@dataclass
class BusNotes:
    raw_notes: str = ""
    timestamp: int = 0
    bus_ids: list = field(default_factory=list)

    def __post_init__(self):
        if self.raw_notes:
            lines = self.raw_notes.strip().splitlines()
            self.timestamp = int(lines.pop(0))
            self.bus_ids = lines.pop(0).split(",")

    @property
    def waiting_product(self):
        valid_ids = [int(id) for id in self.bus_ids if id.isdigit()]
        for t in itertools.count(start=self.timestamp):
            for bus_id in valid_ids:
                if t % bus_id == 0:
                    return (t - self.timestamp) * bus_id

        return math.inf

    @property
    def offset_timestamp(self):
        bus_map = {
            int(bus_id): int(offset)
            for offset, bus_id in enumerate(self.bus_ids)
            if bus_id.isdigit()
        }
        MAX_TIMESTAMP = 100_000_000_000_000

        matches = range(MAX_TIMESTAMP)

        def filter_offsets(n, offset, bus_id):
            logging.debug("Applying filter_offsets with %s, %s, %s", n, offset, bus_id)
            return n + offset in range(0, MAX_TIMESTAMP, bus_id)

        for bus_id, offset in bus_map.items():
            matches = filter(
                lambda n, offset=offset, bus_id=bus_id: filter_offsets(
                    n, offset, bus_id
                ),
                matches,
            )

        return next(matches)


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=13)
    bus_notes = BusNotes(puzzle.input_data)
    puzzle.answer_a = bus_notes.waiting_product
    puzzle.answer_b = bus_notes.offset_timestamp
