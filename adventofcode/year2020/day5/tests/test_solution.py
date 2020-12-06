import pytest

from adventofcode.year2020.day5.solution import BoardingPass, Manifest


@pytest.fixture(name="simple_manifest")
def fixture_simple_manifest():
    return """
FBFBBFFRLR
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL
""".strip()


@pytest.mark.parametrize("code, seat_id", [("FBFBBFFRLR", 357)])
def test_boarding_pass(code, seat_id):
    bp = BoardingPass(code)
    assert bp.seat_id == seat_id


def test_manifest(simple_manifest):
    manifest = Manifest([BoardingPass(code) for code in simple_manifest.split("\n")])
    assert manifest.max_seat_id == 820
