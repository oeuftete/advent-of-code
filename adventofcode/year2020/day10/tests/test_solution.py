import pytest

from adventofcode.year2020.day10.solution import AdapterBag

FIXTURE_SIMPLE_BAG = """
16
10
15
5
1
11
7
19
6
12
4
"""


FIXTURE_INTERMEDIATE_BAG = """
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
"""


@pytest.mark.parametrize(
    "bag,diffs_one,diffs_three,diffs_product,arrangements",
    [
        (FIXTURE_SIMPLE_BAG, 7, 5, 35, 8),
        (FIXTURE_INTERMEDIATE_BAG, 22, 10, 220, 19208),
    ],
)
def test_bags(bag, diffs_one, diffs_three, diffs_product, arrangements):
    adapters = AdapterBag([int(n) for n in bag.strip().splitlines()])
    adapters.chain()
    assert adapters.diffs[1] == diffs_one
    assert adapters.diffs[3] == diffs_three
    assert adapters.diffs_product() == diffs_product
    assert adapters.arrangements == arrangements
