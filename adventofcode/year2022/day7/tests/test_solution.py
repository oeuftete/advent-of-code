import pytest

from adventofcode.year2022.day7.solution import DirReader


@pytest.fixture(name="example_commands")
def fixture_example_commands():
    return """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".strip().splitlines()


def test_example_commands(example_commands):
    dir_reader = DirReader(example_commands)

    #  assert dir_reader.dir_size("/") == 48381165
    #  assert dir_reader.dir_size("a") == 94853
    #  assert dir_reader.dir_size("d") == 24933642
    #  assert dir_reader.dir_size("e") == 584

    assert dir_reader.part_a_solution == 95437
