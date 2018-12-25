import logging
import math
import re

from aocd import get_data
from cached_property import cached_property

logging.basicConfig(level=logging.INFO)


class Bot():
    def __init__(self, **kwargs):
        self.signal = int(kwargs.get('signal', 0))
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

    @cached_property
    def signal_extent(self):
        min_extent = [math.inf] * 3
        max_extent = [-math.inf] * 3
        for b in self.bots:
            b_min = (b.x - b.signal, b.y - b.signal, b.z - b.signal)
            b_max = (b.x + b.signal, b.y + b.signal, b.z + b.signal)
            for i in range(3):
                if b_min[i] < min_extent[i]:
                    min_extent[i] = b_min[i]
                if b_max[i] > max_extent[i]:
                    max_extent[i] = b_max[i]

        return (tuple(min_extent), tuple(max_extent))

    @cached_property
    def most_in_range_distance(self):
        (min_extent, max_extent) = self.signal_extent

        max_in_range = 0
        distance_to_origin = math.inf
        origin_bot = Bot(x=0, y=0, z=0)

        for x in range(min_extent[0], max_extent[0] + 1):
            for y in range(min_extent[1], max_extent[1] + 1):
                for z in range(min_extent[2], max_extent[2] + 1):
                    c_bot = Bot(x=x, y=y, z=z)
                    in_range_of_c = 0
                    for b in self.bots:
                        if c_bot.manhattan_distance(b) <= b.signal:
                            in_range_of_c += 1

                    if in_range_of_c >= max_in_range:
                        max_in_range = in_range_of_c
                        c_to_origin = c_bot.manhattan_distance(origin_bot)
                        if (c_to_origin < distance_to_origin):
                            distance_to_origin = c_to_origin

        return distance_to_origin


if __name__ == '__main__':
    data = get_data(year=2018, day=23)
    print("Problem 1:", len(BotSpace(data).bots_in_range))
    print("Problem 2:", "TBD")
