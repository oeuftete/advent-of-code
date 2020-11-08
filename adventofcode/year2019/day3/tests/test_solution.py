import pytest

from adventofcode.year2019.day3.solution import closest_intersection


@pytest.mark.parametrize(
    "path_one,path_two,optimum,use_steps",
    [
        ("R8,U5,L5,D3", "U7,R6,D4,L4", 6, False),
        (
            "R75,D30,R83,U83,L12,D49,R71,U7,L72",
            "U62,R66,U55,R34,D71,R55,D58,R83",
            159,
            False,
        ),
        (
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
            135,
            False,
        ),
        ("R8,U5,L5,D3", "U7,R6,D4,L4", 30, True),
        (
            "R75,D30,R83,U83,L12,D49,R71,U7,L72",
            "U62,R66,U55,R34,D71,R55,D58,R83",
            610,
            True,
        ),
        (
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
            410,
            True,
        ),
    ],
)
def test_closest_intersection(path_one, path_two, optimum, use_steps):
    assert closest_intersection(path_one, path_two, use_steps) == optimum
