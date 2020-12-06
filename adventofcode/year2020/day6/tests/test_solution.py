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
    "group, any_yeses, all_yeses",
    [
        ("abc", {"a", "b", "c"}, {"a", "b", "c"}),
        ("ab\nac", {"a", "b", "c"}, {"a"}),
        ("a\na\na\na", {"a"}, {"a"}),
    ],
)
def test_customs_form(group, any_yeses, all_yeses):
    assert CustomsGroup(group).any_yeses == any_yeses
    assert CustomsGroup(group).all_yeses == all_yeses


def test_customs_collection(simple_customs_collection):
    cc = CustomsCollection(simple_customs_collection)
    assert len(cc.groups) == 5
    assert len(cc.groups[1].forms) == 3
    assert cc.groups[2].any_yeses == {"a", "b", "c"}
    assert cc.sum_of_any_yeses == 11

    assert cc.groups[0].all_yeses == {"a", "b", "c"}
    assert cc.groups[2].all_yeses == {"a"}
    assert cc.sum_of_all_yeses == 6
