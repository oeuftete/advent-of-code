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
    assert len(bus_notes.bus_ids) == 5
    assert 59 in bus_notes.bus_ids
    assert bus_notes.waiting_product == 295
