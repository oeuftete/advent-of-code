import itertools
import logging
import math
from dataclasses import dataclass, field

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
            int(id): int(offset)
            for offset, id in enumerate(self.bus_ids)
            if id.isdigit()
        }
        id_offset_zero = int(self.bus_ids[0])
        max_id = max(bus_map)
        logging.debug("Searching offset0=%s, max=%s", id_offset_zero, max_id)

        matching_offset = math.inf
        for t in itertools.count(step=id_offset_zero):
            if t > 1_100_000:
                break
            logging.debug("Checking time %s", t)

            try:
                for bus_id, offset in bus_map.items():
                    id_t = t + offset
                    logging.debug("Checking for id %s at %s", bus_id, id_t)
                    if id_t not in range(0, t + bus_id, bus_id):
                        raise StopIteration(f"Time {t} does not match.")
            except StopIteration as e:
                logging.debug("Continuing: %s", e)
                continue

            matching_offset = t
            break

        return matching_offset


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=13)
    bus_notes = BusNotes(puzzle.input_data)
    puzzle.answer_a = bus_notes.waiting_product
    puzzle.answer_b = bus_notes.offset_timestamp
