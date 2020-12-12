import pytest

from adventofcode.year2020.day11.solution import SeatingArea


@pytest.fixture(name="simple_seat_layout")
def fixture_simple_seat_layout():
    return """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
""".strip()


def test_seat_layout(simple_seat_layout):
    seating_area = SeatingArea(simple_seat_layout)
    seating_area.reseat_until_stable()
    assert seating_area.occupied_seats == 37


def test_seat_layout_alt(simple_seat_layout):
    seating_area = SeatingArea(simple_seat_layout)
    seating_area.reseat_until_stable(algorithm="alt")
    assert seating_area.occupied_seats == 26
