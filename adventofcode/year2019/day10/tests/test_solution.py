import pytest

from adventofcode.common.coordinate import Coordinate
from adventofcode.year2019.day10.solution import Line, Asteroid, AsteroidMap


#  simple Line points_on_line tests first.
@pytest.mark.parametrize("start,end,intersections", [
    ((1, 0), (5, 0), [(2, 0), (3, 0), (4, 0)]),
    ((0, 1), (0, 5), [(0, 2), (0, 3), (0, 4)]),
    ((4, 3), (8, 3), [(5, 3), (6, 3), (7, 3)]),
    ((1, 1), (3, 3), [(2, 2)]),
    ((3, 3), (1, 1), [(2, 2)]),
    ((1, 1), (7, 2), []),
    ((7, 2), (7, 2), []),
    ((1, 1), (7, 3), [(4, 2)]),
    ((1, 1), (7, 4), [(3, 2), (5, 3)]),
    ((1, 0), (3, 4), [(2, 2)]),
])
def test_line(start, end, intersections):
    line_points = Line(Coordinate(*start), Coordinate(*end)).points_on_line
    assert line_points == [Coordinate(*i) for i in intersections]


def test_asteroid():
    a = Asteroid(3, 4)
    assert a.x == 3
    assert a.y == 4
    assert a.n_viewable == 0

    a.add_viewable(Asteroid(4, 5))
    assert a.n_viewable == 1


#  TODO: more maps
TEST_MAP = '''.#..#
.....
#####
....#
...##'''


def test_asteroid_map():
    am = AsteroidMap(TEST_MAP)
    assert am.has_asteroid_at(Coordinate(2, 2))
    assert am.has_asteroid_at(Coordinate(3, 4))

    assert am.get_asteroid_at(Coordinate(3, 4)).n_viewable == 8
    assert am.get_asteroid_at(Coordinate(4, 4)).n_viewable == 7

    assert am.best_asteroid == Asteroid(3, 4)
