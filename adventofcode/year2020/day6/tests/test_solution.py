import pytest

from adventofcode.year2020.day6.solution import (
    CustomsCollection,
    CustomsForm,
    CustomsGroup,
)


@pytest.fixture
def simple_customs_collection():
    return """
abc

a
b
c

ab
ac

a
a
a
a

b
""".strip()


@pytest.mark.parametrize("line,answers", [("a", {"a"}), ("ab", {"a", "b"})])
def test_customs_form(line, answers):
    assert CustomsForm(line).answers == answers


@pytest.mark.parametrize(
    "group, yeses",
    [
        ("abc", {"a", "b", "c"}),
        ("ab\nac", {"a", "b", "c"}),
        ("a\na\na\na", {"a"}),
    ],
)
def test_customs_form(group, yeses):
    assert CustomsGroup(group).yeses == yeses


def test_customs_collection(simple_customs_collection):
    cc = CustomsCollection(simple_customs_collection)
    assert len(cc.groups) == 5
    assert len(cc.groups[1].forms) == 3
    assert cc.groups[2].yeses == {"a", "b", "c"}
    assert cc.sum_of_yeses == 11
