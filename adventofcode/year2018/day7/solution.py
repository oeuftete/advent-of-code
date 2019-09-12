import itertools
import logging
import math
import re

from aocd import get_data
import networkx as nx

logging.basicConfig(level=logging.DEBUG)


def parse_step(step):
    STEP_FORMAT = re.compile(
        r'Step (\w) must be finished before step (\w) can begin.')
    m = re.match(STEP_FORMAT, step)
    (preceding, following) = m.groups()
    return (preceding, following)


def get_ordered_step_string(steps):
    g = build_graph(steps)

    s = ""

    all_nodes = list(g.nodes())
    logging.debug("All nodes: {}".format(all_nodes))

    tops = [n for n in g.nodes() if not sorted(list(g.predecessors(n)))]
    logging.debug("Top nodes: {}".format(tops))
    for top in sorted(tops):
        all_nodes.remove(top)
        s += top
        for next_one in find_and_pop_next_nodes(g, top, set(), all_nodes):
            s += next_one

    return s


def find_and_pop_next_nodes(g, node, pending_nodes, all_nodes):
    ordered_nodes = []

    next_nodes = sorted(
        list(filter(lambda x: x in all_nodes, list(g.successors(node)))))
    pending_nodes.update(set(next_nodes))

    logging.debug('Next available nodes: {}'.format(next_nodes))
    logging.debug('All pending nodes: {}'.format(sorted(pending_nodes)))
    for next_node in sorted(pending_nodes):
        logging.debug('Looking at {}...'.format(next_node))
        if next_node in all_nodes:
            logging.debug('... {} still in all_nodes ...'.format(next_node))

            all_next_node_preds = [
                n for n in list(nx.bfs_tree(g, next_node, True))
                if n != next_node
            ]
            preds = list(
                filter(lambda n: n in pending_nodes, all_next_node_preds))
            if preds:
                logging.debug(
                    '... {} has predecessors ({}) in pending_nodes {}...'
                    'skipping'.format(next_node, preds, pending_nodes))
                continue

            logging.debug('{} predecessors ({}) were irrelevant to '
                          'pending nodes {}.  Adding.'.format(
                              next_node, all_next_node_preds, pending_nodes))
            all_nodes.remove(next_node)
            pending_nodes.remove(next_node)
            ordered_nodes.append(next_node)

            recursed = find_and_pop_next_nodes(g, next_node, pending_nodes,
                                               all_nodes)
            if recursed:
                ordered_nodes.extend(recursed)
            elif len(all_nodes) == 1:
                all_nodes.remove(next_node)
                ordered_nodes.append(next_node)

        else:
            logging.debug('... {} was gone'.format(next_node))

    return ordered_nodes


def build_graph(steps):
    g = nx.DiGraph()
    for step in steps:
        (preceding, following) = parse_step(step)
        g.add_edge(preceding, following)

    return g


def build_workload_graph(steps, offset):
    g = nx.DiGraph()

    def add_workload_node(c):
        if c not in g:
            g.add_node(c,
                       cost=step_cost(c, offset),
                       completion=math.inf,
                       worker=None)

    for step in steps:
        (preceding, following) = parse_step(step)
        add_workload_node(preceding)
        add_workload_node(following)
        g.add_edge(preceding, following)

    return g


def assign_work_to_node(g, c, now, worker):
    node_costs = nx.get_node_attributes(g, 'cost')
    g.add_node(c, worker=worker, completion=now + node_costs[c])


def step_cost(c, offset):
    return ord(c) - 64 + offset


def get_build_time(steps, workers, offset):
    g = build_workload_graph(steps, offset)
    s = ""

    for i in itertools.count():

        def cycle_log(msg):
            logging.debug('%04d: [%-26s] %s' % (i, s, msg))

        #  Are any workers done in this second?  If so, delete the node and add
        #  worker
        completions = nx.get_node_attributes(g, 'completion')
        completed = [
            n for n, completion in completions.items() if completion == i
        ]
        cycle_log('Completed = {}'.format(completed))
        for nc in completed:
            cycle_log('Removed = {}'.format(completed))
            g.remove_node(nc)
            workers += 1
            s += nc
            cycle_log('Workers = %d' % workers)
            if not list(g):
                return i

        #  Find the current tops
        tops = [n for n in g.nodes() if not list(g.predecessors(n))]
        for nt in tops:
            cycle_log('Found top %s' % nt)
            if completions[nt] == math.inf and workers > 0:
                cycle_log('Assigning worker %d to %s' % (workers, nt))
                assign_work_to_node(g, nt, i, workers)
                workers -= 1


if __name__ == '__main__':
    steps = get_data(year=2018, day=7).split('\n')
    print("Problem 1:", get_ordered_step_string(steps))
    print("Problem 2:", get_build_time(steps, 5, 60))
