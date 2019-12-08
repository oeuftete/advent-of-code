import pytest

from adventofcode.year2019.day8.solution import (Layer, Image)


@pytest.mark.parametrize("image_data,image_size,layers,solution_a",
                         [("123456789012", (3, 2), [
                             Layer(data='123456', size=(3, 2)),
                             Layer(data='789012', size=(3, 2)),
                         ], 1)])
def test_example_a(image_data, image_size, layers, solution_a):
    image = Image(image_data, size=image_size)
    assert all(map(lambda l1, l2: l1 == l2, image.layers, layers))
    assert image.solution_a == solution_a


def test_example_b():
    image = Image('0222112222120000', (2, 2))
    assert image.rendered == '01\n10'
    assert image.rendered_clearly == u' \u2588\n\u2588 '
