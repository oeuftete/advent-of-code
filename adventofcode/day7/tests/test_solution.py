import pytest

from adventofcode.day7.solution import (
    build_graph,
    get_ordered_step_string,
    parse_step
)


TEST_STEPS = [
    'Step C must be finished before step A can begin.',
    'Step C must be finished before step F can begin.',
    'Step A must be finished before step B can begin.',
    'Step A must be finished before step D can begin.',
    'Step B must be finished before step E can begin.',
    'Step D must be finished before step E can begin.',
    'Step F must be finished before step E can begin.',
]


def test_parse_step():
    assert parse_step(TEST_STEPS[0]) == ("C", "A")


def test_build_graph():
    g = build_graph(TEST_STEPS)
    assert sorted(list(g.nodes())) == ['A', 'B', 'C', 'D', 'E', 'F']

    top = [n for n in g.nodes() if not list(g.predecessors(n))]
    assert top == ['C']
    assert sorted(list(g.successors('C'))) == ['A', 'F']
    assert sorted(list(g.successors('A'))) == ['B', 'D']
    assert not list(g.successors('E'))


@pytest.mark.parametrize("steps,ordered_step_string", [
    (TEST_STEPS, 'CABDFE'),
])
def test_get_ordered_step_string(steps, ordered_step_string):
    assert get_ordered_step_string(steps) == ordered_step_string
