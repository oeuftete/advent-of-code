from collections import defaultdict, deque
import re

from aocd import get_data


def parse_rules(s):
    RULE_FORMAT = (
        r"(\d+) players; "
        r"last marble is worth (\d+) points"
        r"(?:: high score is (\d+))?$"
    )
    m = re.match(RULE_FORMAT, s)
    (players, play_until, high_score) = list(
        map(lambda x: int(x) if x else None, m.groups())
    )
    return (players, play_until, high_score)


class Game:
    def __init__(self, players):
        self.board = deque([0])
        self.player_count = players
        self.players = defaultdict(int)
        self.current_player = 1

    def play_until(self, n):
        for i in range(1, n + 1):
            self.move(i)
        return self

    def move(self, n):
        if n % 23:
            self.normal_move(n)
        else:
            self.special_move(n)

    def normal_move(self, n):
        self.board.rotate(-1)
        self.board.append(n)
        self.next_turn()

    def special_move(self, n):
        self.board.rotate(7)
        removed = self.board.pop()
        self.players[self.current_player] += n + removed
        self.board.rotate(-1)
        self.next_turn()

    def next_turn(self):
        if self.current_player == self.player_count:
            self.current_player = 1
        else:
            self.current_player += 1

    def player_score(self, p):
        return self.players[p]

    def all_player_scores(self):
        return dict(self.players)

    def top_scorer(self):
        return sorted(self.all_player_scores().items(), key=lambda s: -1 * s[1])[0]

    def top_score(self):
        return self.top_scorer()[1]


if __name__ == "__main__":
    (players, play_until, _) = parse_rules(get_data(year=2018, day=9))
    print("Problem 1:", Game(players).play_until(play_until).top_score())
    print("Problem 2:", Game(players).play_until(play_until * 100).top_score())
