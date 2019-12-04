import pytest

from adventofcode.common.coordinate import Coordinate
from adventofcode.year2018.day6.solution import (get_boundaries,
                                                 get_boundary_indices,
                                                 get_bound_indices,
                                                 get_safe_coordinates,
                                                 largest_area)

TEST_COORDINATES = list(
    map(lambda c: Coordinate(csv=c), [
        '1, 1',
        '1, 6',
        '8, 3',
        '3, 4',
        '5, 5',
        '8, 9',
    ]))


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
    assert (len(get_safe_coordinates(coordinates,
                                     threshold)) == safe_coordinate_area)
