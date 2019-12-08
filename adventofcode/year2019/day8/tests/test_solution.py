import pytest

from adventofcode.year2019.day8.solution import (Layer, Image)


@pytest.mark.parametrize("image_data,image_size,layers,solution_a",
                         [("123456789012", (3, 2), [
                             Layer([list('123'), list('456')]),
                             Layer([list('789'), list('012')]),
                         ], 1)])
def test_all(image_data, image_size, layers, solution_a):
    image = Image(image_data, size=image_size)
    assert all(map(lambda l1, l2: l1 == l2, image.layers, layers))
    assert image.solution_a == solution_a
