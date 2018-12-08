import pytest

from adventofcode.day6.solution import (
    Coordinate,
    get_boundaries,
    get_boundary_indices,
    get_bound_indices,
    get_safe_coordinates,
    largest_area
)


def test_coordinate():
    c1 = Coordinate(csv='1, 1')
    assert c1.x == 1
    assert c1.y == 1

    c2 = Coordinate(x=3, y=4)
    assert c2.x == 3
    assert c2.y == 4

    assert c1.manhattan_distance(c2) == 5
    assert c2.manhattan_distance(c1) == 5

    assert c1 < c2
    assert c1 == Coordinate(x=1, y=1)


TEST_COORDINATES = list(map(lambda c: Coordinate(csv=c), [
    '1, 1',
    '1, 6',
    '8, 3',
    '3, 4',
    '5, 5',
    '8, 9',
]))


def test_bounding():
    c_1_1 = Coordinate(x=1, y=1)
    c_2_1 = Coordinate(x=2, y=1)

    assert c_2_1.is_bounded_by(c_1_1, 'west')
    assert not c_2_1.is_bounded_by(c_1_1, 'east')
    assert not c_2_1.is_bounded_by(c_1_1, 'north')
    assert not c_2_1.is_bounded_by(c_1_1, 'south')

    c_2_6 = Coordinate(x=2, y=6)
    assert not c_2_6.is_bounded_by(c_1_1, 'west')
    assert not c_2_6.is_bounded_by(c_1_1, 'east')
    assert not c_2_6.is_bounded_by(c_1_1, 'north')
    assert c_2_6.is_bounded_by(c_1_1, 'south')

    c_5_5 = Coordinate(x=5, y=5)
    assert c_5_5.is_bounded_by(c_1_1, 'west')
    assert not c_5_5.is_bounded_by(c_1_1, 'east')
    assert not c_5_5.is_bounded_by(c_1_1, 'north')
    assert c_5_5.is_bounded_by(c_1_1, 'south')


@pytest.mark.parametrize("coordinates,boundaries", [
    (TEST_COORDINATES, ((1, 8), (1, 9))),
])
def test_boundaries(coordinates, boundaries):
    assert get_boundaries(coordinates) == boundaries


@pytest.mark.parametrize("coordinates,boundary_indices", [
    (TEST_COORDINATES, [0, 1, 2, 5]),
])
def test_boundary_indices(coordinates, boundary_indices):
    assert get_boundary_indices(coordinates) == boundary_indices


@pytest.mark.parametrize("coordinates,bound_indices", [
    (TEST_COORDINATES, [3, 4]),
])
def test_bound_indices(coordinates, bound_indices):
    assert get_bound_indices(coordinates) == bound_indices


@pytest.mark.parametrize("coordinates,area", [
    (TEST_COORDINATES, 17),
])
def test_largest_area(coordinates, area):
    assert largest_area(coordinates) == 17


@pytest.mark.parametrize("coordinates,threshold,safe_coordinate_area", [
    (TEST_COORDINATES, 32, 16),
])
def test_safe_coordinates(coordinates, threshold, safe_coordinate_area):
    assert (len(get_safe_coordinates(coordinates, threshold))
            == safe_coordinate_area)
