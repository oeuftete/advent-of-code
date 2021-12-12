import pytest

from adventofcode.year2021.day12.solution import Cavern


@pytest.fixture(name="example_small")
def fixture_example_small():
    return """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""".strip().splitlines()


@pytest.fixture(name="example_medium")
def fixture_example_medium():
    return """
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
""".strip().splitlines()


@pytest.fixture(name="example_large")
def fixture_example_large():
    return """
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
""".strip().splitlines()


def test_example_small(example_small):
    cavern = Cavern(example_small)

    assert len(cavern.possible_paths) == 10


def test_example_medium(example_medium):
    cavern = Cavern(example_medium)

    assert len(cavern.possible_paths) == 19


def test_example_large(example_large):
    cavern = Cavern(example_large)

    assert len(cavern.possible_paths) == 226
