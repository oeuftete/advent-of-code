import pytest

from adventofcode.common.coordinate import Coordinate
from adventofcode.year2020.day12.solution import NavSystem


@pytest.fixture(name="instructions")
def fixture_instructions():
    return """
F10
N3
F7
R90
F11
""".strip().splitlines()


def test_nav_system(instructions):
    nav_system = NavSystem(instructions)
    assert nav_system.origin == Coordinate(0, 0)
    assert nav_system.location == Coordinate(0, 0)
    assert nav_system.bearing == "east"

    nav_system.process(n=1)
    assert nav_system.location == Coordinate(10, 0)
    assert nav_system.bearing == "east"

    nav_system.process(n=1)
    assert nav_system.location == Coordinate(10, 3)
    assert nav_system.bearing == "east"

    nav_system.process(n=1)
    assert nav_system.location == Coordinate(17, 3)
    assert nav_system.bearing == "east"

    nav_system.process(n=1)
    assert nav_system.location == Coordinate(17, 3)
    assert nav_system.bearing == "south"

    nav_system.process(n=1)
    assert nav_system.location == Coordinate(17, -8)
    assert nav_system.location.manhattan_distance(nav_system.origin) == 25
    assert nav_system.bearing == "south"


def test_nav_system_waypoint(instructions):
    nav_system = NavSystem(instructions, use_waypoint=True)
    assert nav_system.origin == Coordinate(0, 0)
    assert nav_system.location == Coordinate(0, 0)
    assert nav_system.waypoint == Coordinate(10, 1)

    nav_system.process(n=1)
    assert nav_system.location == Coordinate(100, 10)
    assert nav_system.waypoint == Coordinate(10, 1)

    nav_system.process(n=1)
    assert nav_system.location == Coordinate(100, 10)
    assert nav_system.waypoint == Coordinate(10, 4)

    nav_system.process(n=1)
    assert nav_system.location == Coordinate(170, 38)
    assert nav_system.waypoint == Coordinate(10, 4)

    nav_system.process(n=1)
    assert nav_system.location == Coordinate(170, 38)
    assert nav_system.waypoint == Coordinate(4, -10)

    nav_system.process(n=1)
    assert nav_system.location == Coordinate(214, -72)
    assert nav_system.waypoint == Coordinate(4, -10)

    assert nav_system.location.manhattan_distance(nav_system.origin) == 286
