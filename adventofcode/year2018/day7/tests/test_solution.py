import networkx as nx
import pytest

from adventofcode.year2018.day7.solution import (
    assign_work_to_node, build_graph, build_workload_graph, get_build_time,
    get_ordered_step_string, parse_step, step_cost)

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


def test_workload_graph():
    g = build_workload_graph(TEST_STEPS, 0)
    top = [n for n in g.nodes() if not list(g.predecessors(n))]
    assert top == ['C']
    assert sorted(list(g.successors('C'))) == ['A', 'F']

    node_costs = nx.get_node_attributes(g, 'cost')
    assert node_costs['C'] == 3
    assert node_costs['F'] == 6

    node_workers = nx.get_node_attributes(g, 'worker')
    assert node_workers['C'] is None

    assign_work_to_node(g, 'C', 10, 7)
    node_completions = nx.get_node_attributes(g, 'completion')
    node_workers = nx.get_node_attributes(g, 'worker')

    assert node_workers['C'] == 7
    assert node_completions['C'] == 13


@pytest.mark.parametrize("steps,ordered_step_string", [
    (TEST_STEPS, 'CABDFE'),
])
def test_get_ordered_step_string(steps, ordered_step_string):
    assert get_ordered_step_string(steps) == ordered_step_string


@pytest.mark.parametrize("c,offset,cost", [
    ('A', 0, 1),
    ('A', 60, 61),
    ('Z', 0, 85),
])
def test_step_cost(c, offset, cost):
    return step_cost(c, offset) == cost


@pytest.mark.parametrize("steps,workers,offset,seconds", [
    (TEST_STEPS, 2, 0, 15),
])
def test_build_time(steps, workers, offset, seconds):
    assert get_build_time(steps, workers, offset) == seconds
