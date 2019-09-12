from itertools import groupby

from adventofcode.common.helpers import day_data


def box_checksum(box_ids):
    doubles = filter(lambda b: box_id_counter(b, 2), box_ids)
    triples = filter(lambda b: box_id_counter(b, 3), box_ids)
    return len(list(doubles)) * len(list(triples))


def common_letters_for_close(box_ids):
    longest_id = len(sorted(box_ids, key=lambda x: len(x), reverse=True)[0])
    for c_pos in range(0, longest_id):
        seen = list()
        for box_id in box_ids:
            b_sliced = box_id[0:c_pos] + box_id[c_pos + 1:]
            if b_sliced in seen:
                return b_sliced
            seen.append(b_sliced)


def box_id_counter(box_id, repeat_count):
    for _, c_group in groupby(sorted(list(box_id))):
        c_count = len(list(c_group))
        if c_count == repeat_count:
            return True

    return False


if __name__ == '__main__':
    box_ids = day_data(2)
    print("Problem 1:", box_checksum(box_ids))
    print("Problem 2:", common_letters_for_close(box_ids))
