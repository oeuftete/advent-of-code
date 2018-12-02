from functools import reduce
from itertools import cycle
import os

from adventofcode.common.helpers import read_input


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
    INPUT_DATA_FILE = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..', '..', 'input/input-day1.txt'
    )
    frequencies = read_input(INPUT_DATA_FILE)
    print("Problem 1:", frequency_summer(frequencies))
    print("Problem 2:", frequency_repeat_checker(frequencies))
