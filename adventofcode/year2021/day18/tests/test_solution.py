import pytest

from adventofcode.year2021.day18.solution import SnailfishNumber


@pytest.mark.parametrize(
    "raw,reduced",
    [
        ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
        ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
        ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
        ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"),
        ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"),
    ],
)
def test_explosions(raw, reduced):
    sn = SnailfishNumber(raw)
    sn.reduce(1)
    assert sn.current == reduced
