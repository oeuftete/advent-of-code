import pytest

from adventofcode.common.coordinate import Coordinate


def test_coordinate():
    c1 = Coordinate(csv="1, 1")
    assert c1.x == 1
    assert c1.y == 1

    c2 = Coordinate(x=3, y=4)
    assert c2.x == 3
    assert c2.y == 4

    assert c1.manhattan_distance(c2) == 5
    assert c2.manhattan_distance(c1) == 5

    assert c1 < c2
    assert c1 == Coordinate(x=1, y=1)

    c3 = Coordinate(5, 6)
    assert str(c3) == "(5, 6)"


def test_bounding():
    c_1_1 = Coordinate(x=1, y=1)
    c_2_1 = Coordinate(x=2, y=1)

    assert c_2_1.is_bounded_by(c_1_1, "west")
    assert not c_2_1.is_bounded_by(c_1_1, "east")
    assert not c_2_1.is_bounded_by(c_1_1, "north")
    assert not c_2_1.is_bounded_by(c_1_1, "south")

    c_2_6 = Coordinate(x=2, y=6)
    assert not c_2_6.is_bounded_by(c_1_1, "west")
    assert not c_2_6.is_bounded_by(c_1_1, "east")
    assert not c_2_6.is_bounded_by(c_1_1, "north")
    assert c_2_6.is_bounded_by(c_1_1, "south")

    c_5_5 = Coordinate(x=5, y=5)
    assert c_5_5.is_bounded_by(c_1_1, "west")
    assert not c_5_5.is_bounded_by(c_1_1, "east")
    assert not c_5_5.is_bounded_by(c_1_1, "north")
    assert c_5_5.is_bounded_by(c_1_1, "south")

    with pytest.raises(ValueError):
        c_2_1.is_bounded_by(c_1_1, "up")
