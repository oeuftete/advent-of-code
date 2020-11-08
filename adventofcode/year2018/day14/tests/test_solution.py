import pytest

from adventofcode.year2018.day14.solution import RecipeScoreboard


def test_scoreboard():
    scoreboard = RecipeScoreboard()

    assert scoreboard.scores == [3, 7]
    assert scoreboard.pointers == [0, 1]

    scoreboard.make_new_recipes()
    assert scoreboard.scores == [3, 7, 1, 0]
    assert scoreboard.pointers == [0, 1]

    scoreboard.make_new_recipes()
    assert scoreboard.scores == [3, 7, 1, 0, 1, 0]
    assert scoreboard.pointers == [4, 3]

    scoreboard.make_new_recipes()
    assert scoreboard.scores == [3, 7, 1, 0, 1, 0, 1]
    assert scoreboard.pointers == [6, 4]

    scoreboard.make_new_recipes()
    assert scoreboard.scores == [3, 7, 1, 0, 1, 0, 1, 2]
    assert scoreboard.pointers == [0, 6]

    scoreboard.make_new_recipes()
    assert scoreboard.scores == [3, 7, 1, 0, 1, 0, 1, 2, 4]
    assert scoreboard.pointers == [4, 8]


@pytest.mark.parametrize(
    "n,next_ten",
    [
        (5, "0124515891"),
        (9, "5158916779"),
        (18, "9251071085"),
        (2018, "5941429882"),
    ],
)
def test_next_ten_scores(n, next_ten):
    scoreboard = RecipeScoreboard()
    assert scoreboard.ten_after(n) == next_ten


@pytest.mark.parametrize(
    "target,n",
    [
        ("01245", 5),
        ("51589", 9),
        ("515891", 9),
        ("92510", 18),
        ("59414", 2018),
    ],
)
def test_preceding_recipes(target, n):
    scoreboard = RecipeScoreboard()
    assert scoreboard.preceding(target) == n
