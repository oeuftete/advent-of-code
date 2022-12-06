from collections import Counter
from itertools import count, islice

import attr
from aocd.models import Puzzle


@attr.s
class StreamReader:
    stream: str = attr.ib()
    first_packet_position: int = attr.ib(default=-1, init=False)
    first_message_position: int = attr.ib(default=-1, init=False)

    def __attrs_post_init__(self) -> None:
        self.process()

    def process(self) -> None:
        for i in count():
            if i > len(self.stream):
                raise ValueError("Did not find expected markers in stream!")

            c_packet = Counter(islice(self.stream, i, i + 4))
            if self.first_packet_position < 0 and all(
                n == 1 for n in c_packet.values()
            ):
                self.first_packet_position = i + 4

            c_message = Counter(islice(self.stream, i, i + 14))
            if self.first_message_position < 0 and all(
                n == 1 for n in c_message.values()
            ):
                self.first_message_position = i + 14

            if self.first_packet_position > 0 and self.first_message_position > 0:
                return


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=6)
    stream_reader = StreamReader(puzzle.input_data.strip())
    puzzle.answer_a = stream_reader.first_packet_position
    puzzle.answer_b = stream_reader.first_message_position
