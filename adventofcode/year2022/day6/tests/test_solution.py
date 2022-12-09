import pytest

from adventofcode.year2022.day6.solution import StreamReader


@pytest.mark.parametrize(
    "stream,first_packet_position,first_message_position",
    [
        ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7, 19),
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23),
        ("nppdvjthqldpwncqszvftbrmjlhg", 6, 23),
        ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26),
    ],
)
def test_streams(stream, first_packet_position, first_message_position):
    assert StreamReader(stream).first_packet_position == first_packet_position
    assert StreamReader(stream).first_message_position == first_message_position
