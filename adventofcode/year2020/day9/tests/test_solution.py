import pytest

from adventofcode.year2020.day9.solution import Cyphertext


@pytest.fixture(name="sample_stream")
def fixture_sample_stream():
    return """
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
""".strip().splitlines()


def test_sample_stream(sample_stream):
    cyphertext = Cyphertext(stream=sample_stream, window_size=5)
    assert cyphertext.first_invalid == 127
