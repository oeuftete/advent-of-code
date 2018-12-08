import logging
import re

from aocd import get_data
import networkx as nx


logging.basicConfig(level=logging.DEBUG)


def parse_step(step):
    STEP_FORMAT = re.compile(
        r'Step (\w) must be finished before step (\w) can begin.'
    )
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

    next_nodes = sorted(list(filter(lambda x: x in all_nodes,
                                    list(g.successors(node)))))
    pending_nodes.update(set(next_nodes))

    logging.debug('Next available nodes: {}'.format(next_nodes))
    logging.debug('All pending nodes: {}'.format(sorted(pending_nodes)))
    for next_node in sorted(pending_nodes):
        logging.debug('Looking at {}...'.format(next_node))
        if next_node in all_nodes:
            logging.debug('... {} still in all_nodes ...'.format(next_node))

            all_next_node_preds = [n for n in
                                   list(nx.bfs_tree(g, next_node, True))
                                   if n != next_node]
            preds = list(filter(lambda n: n in pending_nodes,
                                all_next_node_preds))
            if preds:
                logging.debug(
                    '... {} has predecessors ({}) in pending_nodes {}...'
                    'skipping'.format(next_node, preds, pending_nodes))
                continue

            logging.debug('{} predecessors ({}) were irrelevant to '
                          'pending nodes {}.  Adding.'
                          .format(next_node, all_next_node_preds,
                                  pending_nodes))
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
    # edges = list()
    g = nx.DiGraph()
    for step in steps:
        (preceding, following) = parse_step(step)
        g.add_edge(preceding, following)

    return g


if __name__ == '__main__':
    steps = get_data(year=2018, day=7).split('\n')
    print("Problem 1:", get_ordered_step_string(steps))
    print("Problem 2:", "TBD")
