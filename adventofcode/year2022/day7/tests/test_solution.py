import pytest
from aocd.models import Puzzle

from adventofcode.year2022.day7.solution import DirReader

EXAMPLE = Puzzle(year=2022, day=7).examples[0]


@pytest.fixture(name="example_commands")
def fixture_example_commands():
    return EXAMPLE.input_data


def test_example_commands(example_commands):
    dir_reader = DirReader(example_commands.splitlines())

    assert dir_reader.dir_size(dir_reader.root) == 48381165
    assert dir_reader.dir_size(dir_reader.find_inode(["a"])) == 94853
    assert dir_reader.dir_size(dir_reader.find_inode(["a", "e"])) == 584
    assert dir_reader.dir_size(dir_reader.find_inode(["d"])) == 24933642

    assert dir_reader.node_dir_sizes() == [
        584,
        94853,
        24933642,
        48381165,
    ]

    assert dir_reader.part_a_solution == int(EXAMPLE.answer_a)
    assert dir_reader.part_b_solution == int(EXAMPLE.answer_b)
