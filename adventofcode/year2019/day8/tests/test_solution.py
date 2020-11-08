import pytest

from adventofcode.year2019.day8.solution import Image, Layer


@pytest.mark.parametrize(
    "layer_data,is_equal",
    [(("123456", "123456"), True), (("123456", "789012"), False),],
)
def test_layer_equality(layer_data, is_equal):
    assert (
        Layer(data=layer_data[0], size=(3, 2)) == Layer(data=layer_data[1], size=(3, 2))
    ) is is_equal


def test_bad_layer_construction():
    with pytest.raises(AssertionError):
        Layer(data="12345", size=(3, 2))


def test_bad_image_construction():
    with pytest.raises(AssertionError):
        Layer(data="12345678901", size=(3, 2))


@pytest.mark.parametrize(
    "image_data,image_size,layers,solution_a",
    [
        (
            "123456789012",
            (3, 2),
            [Layer(data="123456", size=(3, 2)), Layer(data="789012", size=(3, 2)),],
            1,
        )
    ],
)
def test_example_a(image_data, image_size, layers, solution_a):
    image = Image(image_data, size=image_size)
    assert all(map(lambda l1, l2: l1 == l2, image.layers, layers))
    assert image.solution_a == solution_a


def test_example_b():
    image = Image("0222112222120000", (2, 2))
    assert image.rendered == "01\n10"
    assert image.rendered_clearly == u" \u2588\n\u2588 "
