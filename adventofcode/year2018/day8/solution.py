import logging
from collections import deque

from anytree import NodeMixin
from aocd import get_data

logging.basicConfig(level=logging.INFO)


class AdventNodeBase(object):
    pass


class AdventNode(AdventNodeBase, NodeMixin):
    def __init__(self, name, parent=None):
        super(AdventNode, self).__init__()
        self.name = name
        self.parent = parent
        self.metadata = list()

    def __str__(self):
        return self.name + ("" if self.is_leaf else "*")

    def __repr__(self):
        return self.__str__()

    def update_metadata(self, metadata):
        self.metadata = metadata

    def node_metadata_sum(self):
        return sum(self.metadata)

    def tree_metadata_sum(self):
        return self.node_metadata_sum() + sum(
            [sum(d.metadata) for d in self.descendants]
        )

    def tree_part2_value(self):
        logging.debug("part2 value: %s" % self.name)
        if self.is_leaf:
            logging.debug("part2 value: %s (leaf)" % self.name)
            return self.node_metadata_sum()
        else:
            logging.debug("part2 value: %s (parent)" % self.name)
            children = self.children
            logging.debug("part2 value: {} children = {}".format(self.name, children))
            logging.debug(
                "part2 value: {} metadata = {}".format(self.name, self.metadata)
            )
            total = 0
            for i in self.metadata:
                try:
                    total += children[i - 1].tree_part2_value()
                except IndexError:
                    pass
            return total


def find_and_process_child(tokens, depth, n, parent_node=None):
    parent = parent_node if parent_node else None
    advent_node = AdventNode("%s:%s" % (depth, n), parent=parent)

    def depth_log(msg):
        logging.debug("%2d:%d %s" % (depth, n, msg))

    def take_metadata(nm):
        metadata = list()
        depth_log("Taking %d metadata" % nm)
        for _ in range(nm):
            metadata.append(tokens.popleft())
        return metadata

    depth_log("Tokens: {}".format(tokens))
    n_children = tokens.popleft()
    n_metadata = tokens.popleft()
    depth_log("Found %d children and %d metadata..." % (n_children, n_metadata))
    depth_log("Tokens: {}".format(tokens))

    if n_children == 0:
        advent_node.update_metadata(take_metadata(n_metadata))
    else:
        for i in range(n_children):
            depth_log("Tokens: {}".format(tokens))
            depth_log("Finding child %d..." % i)
            depth += 1
            find_and_process_child(tokens, depth, i, advent_node)
        advent_node.update_metadata(take_metadata(n_metadata))

    return advent_node


def sum_all_metadata(tree_data):
    tree = build_tree(tree_data)
    return tree.tree_metadata_sum()


def build_tree(tree_data):
    return find_and_process_child(deque(list(map(int, tree_data.split()))), 0, 0)


def get_root_node_value(tree_data):
    tree = build_tree(tree_data)
    return tree.tree_part2_value()


if __name__ == "__main__":
    tree_data = get_data(year=2018, day=8)
    print("Problem 1:", sum_all_metadata(tree_data))
    print("Problem 2:", get_root_node_value(tree_data))
