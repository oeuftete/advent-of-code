#  import logging
import math
import re

from cached_property import cached_property
import networkx as nx


class Nanofactory(object):
    def __init__(self, input_reactions):
        self.g = nx.DiGraph()
        self.ORIGIN = "FUEL"

        if isinstance(input_reactions, str):
            input_reactions = input_reactions.split("\n")
        self.input_reactions = input_reactions

        self._build_graph()

    def _build_graph(self):
        REACTION_FORMAT = re.compile(r"(.*?) => (.*)")
        REACTANT_FORMAT = re.compile(r"(\d+) (\w+)")
        for reaction in self.input_reactions:
            m_reactants = re.match(REACTION_FORMAT, reaction)
            inputs, output = m_reactants.groups()

            m_output = re.match(REACTANT_FORMAT, output)
            n_output, output_reactant = m_output.groups()

            #  On the node, n is the number of output reactants generated
            self.g.add_node(output_reactant, n=n_output, reserves=0)

            for input_string in [s.strip() for s in inputs.split(",")]:
                m_input = re.match(REACTANT_FORMAT, input_string)
                n_input, input_reactant = m_input.groups()
                #  On the edge, n is the number of input reactants required,
                #  and cost is the total cost.
                self.g.add_edge(
                    output_reactant, input_reactant, n=n_output, cost=n_input
                )

            #  We have as much ORE as we need
            self.g.add_node("ORE", reserves=math.inf)

    @cached_property
    def minimum_ore(self):
        for p in nx.all_simple_paths(self.g, "FUEL", "ORE"):
            #  Traversing the edges this way isn't what's required.  Need to
            #  figure it out.
            pass
