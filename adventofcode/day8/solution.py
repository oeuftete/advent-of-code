from collections import deque
import logging

from aocd import get_data


logging.basicConfig(level=logging.INFO)


def find_and_process_child(tokens, depth):

    def depth_log(msg):
        logging.debug('%2d: %s' % (depth, msg))

    def take_metadata(n):
        metadata_total = 0
        depth_log('Taking %d metadata' % n)
        for _ in range(n):
            metadata_total += tokens.popleft()
        depth_log('... totalling %d' % metadata_total)
        return metadata_total

    depth_log('Tokens: {}'.format(tokens))
    n_children = tokens.popleft()
    n_metadata = tokens.popleft()
    depth_log('Found %d children and %d metadata...' % (n_children,
                                                        n_metadata))
    depth_log('Tokens: {}'.format(tokens))

    total = 0

    if n_children == 0:
        total += take_metadata(n_metadata)
    else:
        for i in range(n_children):
            depth_log('Tokens: {}'.format(tokens))
            depth_log('Finding child %d...' % i)
            depth += 1
            total += find_and_process_child(tokens, depth)
        total += take_metadata(n_metadata)

    return total


def sum_all_metadata(tree_data):
    return find_and_process_child(deque(list(map(int, tree_data.split()))),
                                  0)


if __name__ == '__main__':
    tree_data = get_data(year=2018, day=8)
    print("Problem 1:", sum_all_metadata(tree_data))
    print("Problem 2:", "TBD")
