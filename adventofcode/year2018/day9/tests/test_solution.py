import pytest

from adventofcode.year2018.day9.solution import (parse_rules, Game)

TEST_GAME_OUTCOMES = [
    '9 players; last marble is worth 25 points: high score is 32',
    '10 players; last marble is worth 1618 points: high score is 8317',
    '13 players; last marble is worth 7999 points: high score is 146373',
    '17 players; last marble is worth 1104 points: high score is 2764',
    '21 players; last marble is worth 6111 points: high score is 54718',
    '30 players; last marble is worth 5807 points: high score is 37305',
]


@pytest.mark.parametrize(
    "game_rules,players,play_until,high_score",
    [(TEST_GAME_OUTCOMES[0], 9, 25, 32),
     ('10 players; last marble is worth 1000 points', 10, 1000, None)])
def test_parse(game_rules, players, play_until, high_score):
    assert parse_rules(game_rules) == (players, play_until, high_score)


@pytest.mark.parametrize("game_rules,players,play_until,high_score", [
    (TEST_GAME_OUTCOMES[0], 9, 25, 32),
    (TEST_GAME_OUTCOMES[1], 10, 1618, 8317),
    (TEST_GAME_OUTCOMES[2], 13, 7999, 146373),
    (TEST_GAME_OUTCOMES[3], 17, 1104, 2764),
    (TEST_GAME_OUTCOMES[4], 21, 6111, 54718),
    (TEST_GAME_OUTCOMES[5], 30, 5807, 37305),
])
def test_game(game_rules, players, play_until, high_score):
    g = Game(players).play_until(play_until)
    assert g.top_score() == high_score
