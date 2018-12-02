from itertools import groupby
import os

from adventofcode.common.helpers import read_input


def box_checksum(box_ids):
    doubles = filter(lambda b: box_id_counter(b, 2), box_ids)
    triples = filter(lambda b: box_id_counter(b, 3), box_ids)
    return len(list(doubles))*len(list(triples))


def box_id_counter(box_id, repeat_count):
    for _, c_group in groupby(sorted(list(box_id))):
        c_count = len(list(c_group))
        if c_count == repeat_count:
            return True

    return False


if __name__ == '__main__':
    INPUT_DATA_FILE = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..', '..', 'input/input-day2.txt'
    )
    box_ids = read_input(INPUT_DATA_FILE)
    print("Problem 1:", box_checksum(box_ids))
