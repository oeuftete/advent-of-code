import pytest

from adventofcode.year2020.day15.solution import NumberGame


@pytest.fixture(name="simple_numbers")
def fixture_simple_numbers():
    return [0, 3, 6]


def test_number_game(simple_numbers):
    game = NumberGame(simple_numbers[:])

    for spoken in [0, 3, 6, 0, 3, 3, 1, 0, 4, 0]:
        game.take_turn(1)
        assert game.spoken == spoken

    game = NumberGame(simple_numbers[:])
    game.take_turn(2020)
    assert game.spoken == 436


@pytest.mark.parametrize(
    "starting,last_spoken",
    [
        ([1, 3, 2], 1),
        ([2, 1, 3], 10),
        ([1, 2, 3], 27),
        ([2, 3, 1], 78),
        ([3, 2, 1], 438),
        ([3, 1, 2], 1836),
    ],
)
def test_other_games(starting, last_spoken):
    game = NumberGame(starting[:])
    game.take_turn(2020)
    assert game.spoken == last_spoken
