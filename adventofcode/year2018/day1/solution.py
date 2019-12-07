from functools import reduce
from itertools import cycle

from aocd.models import Puzzle


def frequency_summer(freq_deltas):
    return reduce(lambda x, y: x + y, map(int, freq_deltas))


def frequency_repeat_checker(freq_deltas):
    current_frequency = 0
    frequencies_seen = set([current_frequency])
    for x in cycle(map(int, freq_deltas)):
        current_frequency += x
        if current_frequency in frequencies_seen:
            return current_frequency
        frequencies_seen.add(current_frequency)


if __name__ == '__main__':
    frequencies = Puzzle(year=2018, day=1).input_data.split('\n')
    print("Problem 1:", frequency_summer(frequencies))
    print("Problem 2:", frequency_repeat_checker(frequencies))
