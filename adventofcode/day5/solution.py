import logging
import os

from adventofcode.common.helpers import read_input


logging.basicConfig(level=logging.INFO)


def reacted_polymer(polymer):
    reacted = polymer[0]

    for unit in polymer[1:]:

        logging.debug('Before reaction: %s + %s' % (reacted[-10:], unit))
        # We have reactants.  Consume each other
        if len(reacted) and unit.swapcase() == reacted[-1]:
            reacted = reacted[:-1]
        else:
            reacted += unit
        logging.debug('After reaction: %s' % reacted[-10:])

    return reacted


if __name__ == '__main__':
    INPUT_DATA_FILE = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..', '..', 'input/input-day5.txt'
    )
    polymer = read_input(INPUT_DATA_FILE)[0]
    print("Problem 1:", len(reacted_polymer(polymer)))
    print("Problem 2:", 'TODO')
