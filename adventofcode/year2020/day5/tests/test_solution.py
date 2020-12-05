import pytest

from adventofcode.year2020.day5.solution import BoardingPass, Manifest


@pytest.fixture
def simple_manifest():
    return """
FBFBBFFRLR
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL
""".strip()


@pytest.mark.parametrize("code, row, column, seat_id", [("FBFBBFFRLR", 44, 5, 357)])
def test_boarding_pass(code, row, column, seat_id):
    bp = BoardingPass(code)
    assert bp.row_number == row
    assert bp.column_number == column
    assert bp.seat_id == seat_id


def test_manifest(simple_manifest):
    manifest = Manifest([BoardingPass(code) for code in simple_manifest.split("\n")])
    assert manifest.max_seat_id == 820
