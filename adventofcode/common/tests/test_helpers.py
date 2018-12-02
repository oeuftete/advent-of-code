import os

from adventofcode.common.helpers import read_input


def test_read_input():
    assert read_input(
        os.path.join(os.path.dirname(os.path.realpath(__file__)),
                     'test_input.txt')
    ) == ['-1', '+1', '-2']
