import pytest

from adventofcode.common.coordinate import Coordinate
from adventofcode.year2019.day10.solution import Asteroid, AsteroidMap, Line


#  simple Line points_on_line tests first.
@pytest.mark.parametrize(
    "start,end,intersections",
    [
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
    ],
)
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
TEST_MAP = """
.#..#
.....
#####
....#
...##
""".strip()


def test_asteroid_map():
    am = AsteroidMap(TEST_MAP)
    assert am.width == 5
    assert am.height == 5

    assert am.get_asteroid_at(Coordinate(0, 0)) == None
    assert am.get_asteroid_at(Coordinate(3, 4)).n_viewable == 8
    assert am.get_asteroid_at(Coordinate(4, 4)).n_viewable == 7

    assert am.best_asteroid == Asteroid(3, 4)


BIG_TEST_MAP = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
""".strip()


@pytest.mark.slow
def test_big_map():
    am = AsteroidMap(BIG_TEST_MAP)
    assert am.width == 20
    assert am.height == 20
    assert am.get_asteroid_at(Coordinate(11, 13)).n_viewable == 210
    assert am.station == Asteroid(11, 13)

    am.run_vaporizer()
    assert am.vaporized[0] == Asteroid(11, 12)
    assert am.vaporized[1] == Asteroid(12, 1)
    assert am.vaporized[19] == Asteroid(16, 0)
    assert am.vaporized[49] == Asteroid(16, 9)
    assert am.vaporized[99] == Asteroid(10, 16)
    assert am.vaporized[198] == Asteroid(9, 6)
    assert am.vaporized[199] == Asteroid(8, 2)


VAPORIZE_TEST_MAP = """
.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##
""".strip()


def test_vaporize_map():
    am = AsteroidMap(VAPORIZE_TEST_MAP)
    assert am.station == Asteroid(8, 3)

    am.run_vaporizer()
    assert am.vaporized[0] == Asteroid(8, 1)
    assert am.vaporized[17] == Asteroid(4, 4)
    assert am.vaporized[26] == Asteroid(5, 1)
    assert am.vaporized[-2] == Asteroid(13, 3)
    assert am.vaporized[-1] == Asteroid(14, 3)
