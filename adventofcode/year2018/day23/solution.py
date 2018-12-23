import logging
import re

from aocd import get_data
from cached_property import cached_property

logging.basicConfig(level=logging.INFO)


class Bot():
    def __init__(self, **kwargs):
        self.signal = int(kwargs['signal'])
        if kwargs.get('csv', None):
            (self.x, self.y,
             self.z) = map(int, kwargs['csv'].replace(" ", "").split(","))
        else:
            self.x = kwargs['x']
            self.y = kwargs['y']
            self.z = kwargs['z']

    def manhattan_distance(self, other):
        return (abs(self.x - other.x) + abs(self.y - other.y) +
                abs(self.z - other.z))

    def __str__(self):
        return "({}, {}, {}) ({})".format(self.x, self.y, self.z, self.signal)


class BotSpace():
    def __init__(self, data):
        self.bots = list()
        self.parse_data(data)

    def parse_data(self, data):
        BOT_LINE = re.compile(r'pos=<(.*?)>, r=(\d+)')
        for l in data.strip().split('\n'):
            m = re.match(BOT_LINE, l)
            (csv, signal) = m.groups()
            self.bots.append(Bot(csv=csv, signal=signal))

    @cached_property
    def strongest_bot(self):
        return sorted(self.bots, key=lambda b: b.signal, reverse=True)[0]

    @cached_property
    def bots_in_range(self):
        return list(
            filter((lambda b: b.manhattan_distance(self.strongest_bot) <= self.
                    strongest_bot.signal), self.bots))


if __name__ == '__main__':
    data = get_data(year=2018, day=23)
    print("Problem 1:", len(BotSpace(data).bots_in_range))
    print("Problem 2:", "TBD")
