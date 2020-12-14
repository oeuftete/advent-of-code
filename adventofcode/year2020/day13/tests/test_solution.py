import pytest

from adventofcode.year2020.day13.solution import BusNotes


@pytest.fixture(name="simple_raw_notes")
def fixture_raw_notes():
    return """
939
7,13,x,x,59,x,31,19
""".strip()


def test_bus_notes(simple_raw_notes):
    bus_notes = BusNotes(simple_raw_notes)
    assert bus_notes.timestamp == 939
    assert len(bus_notes.bus_ids) == 8
    assert "59" in bus_notes.bus_ids
    assert bus_notes.waiting_product == 295


@pytest.mark.parametrize(
    "bus_ids,offset_timestamp",
    [
        # ("7,13,x,x,59,x,31,19", 1068781),
        ("17,x,13,19", 3417),
        ("67,7,59,61", 754018),
        # ("67,x,7,59,61", 779210),
        # ("67,7,x,59,61", 1261476),
        # ("1789,37,47,1889", 1202161486),
    ],
)
def test_offset_timestamp(bus_ids, offset_timestamp):
    bus_notes = BusNotes(bus_ids=bus_ids.split(","))
    assert bus_notes.offset_timestamp == offset_timestamp
