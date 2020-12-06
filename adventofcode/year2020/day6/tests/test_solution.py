import pytest

from adventofcode.year2020.day6.solution import (
    CustomsCollection,
    CustomsForm,
    CustomsGroup,
)


@pytest.fixture(name="simple_customs_collection")
def fixture_simple_customs_collection():
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
def test_customs_group(group, any_yeses, all_yeses):
    assert CustomsGroup(group).any_yeses == any_yeses
    assert CustomsGroup(group).all_yeses == all_yeses


def test_customs_collection(simple_customs_collection):
    customs_collection = CustomsCollection(simple_customs_collection)
    assert len(customs_collection.groups) == 5
    assert len(customs_collection.groups[1].forms) == 3
    assert customs_collection.groups[2].any_yeses == {"a", "b", "c"}
    assert customs_collection.sum_of_any_yeses == 11

    assert customs_collection.groups[0].all_yeses == {"a", "b", "c"}
    assert customs_collection.groups[2].all_yeses == {"a"}
    assert customs_collection.sum_of_all_yeses == 6
