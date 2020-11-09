import logging
import math
import re

import networkx as nx
from cached_property import cached_property


class Nanofactory(object):
    def __init__(self, input_reactions):
        self.g = nx.DiGraph()
        self.ORIGIN = "FUEL"

        if isinstance(input_reactions, str):
            input_reactions = input_reactions.split("\n")
        self.input_reactions = input_reactions

        self.ore_requests = []

        self._build_graph()

    def _build_graph(self):
        #  We have as much ORE as we need
        self.g.add_node("ORE", reserve=math.inf)

        REACTION_FORMAT = re.compile(r"(.*?) => (.*)")
        REACTANT_FORMAT = re.compile(r"(\d+) (\w+)")
        for reaction in self.input_reactions:
            m_reactants = re.match(REACTION_FORMAT, reaction)
            inputs, output = m_reactants.groups()

            m_output = re.match(REACTANT_FORMAT, output)
            n_output, output_reactant = m_output.groups()

            self.g.add_node(output_reactant, reserve=0)

            for input_string in [s.strip() for s in inputs.split(",")]:
                m_input = re.match(REACTANT_FORMAT, input_string)
                n_input, input_reactant = m_input.groups()
                #  On the edge, n is the number of input reactants required,
                #  and cost is the total cost.
                self.g.add_edge(
                    output_reactant,
                    input_reactant,
                    n=int(n_output),
                    cost=int(n_input),
                )

    def reset(self):
        for n in self.g.nodes():
            self.g.nodes[n]["reserve"] = 0

    def minimum_ore_for_chemical(self, chemical="FUEL", n=1, top_level=True):
        # Start at `chemical`
        #
        # Figure out the cost in immediate precursors.
        # For each precursor that's not ORE, recursively call this f
        # If it's ORE, add an item in ore withdrawal, don't add these together.
        #
        # E.g. for the example with FUEL:
        #   - Add costs: 1E, 7A
        #     - Add costs: 1D, 7A
        #       - Add costs: 1C, 7A
        #         - Add costs: 1B, 7A
        #           - Add costs: 1 ORE (now [1B])
        #           - Add costs: 7 ORE (now [1B, 7A])
        #         - Add costs: 7 ORE (now [1B, 7A, 7A])
        #       - Add costs: 7 ORE (now [1B, 7A, 7A, 7A])
        #     - Add costs: 7 ORE (now [1B, 7A, 7A, 7A, 7A])

        logging.debug(f"Determining ORE requirement for {n} {chemical}")
        logging.debug(self.g.edges([chemical], data=True))
        for _, precursor, reaction_data in self.g.edges([chemical], data=True):
            logging.debug(f"... precursor found: {precursor}: {reaction_data}")
            if precursor == "ORE":
                logging.debug(f"Adding ORE request for {n} {chemical}.")
                self.ore_requests.append(
                    (chemical, n, reaction_data["cost"], reaction_data["n"])
                )
            else:
                cost = reaction_data["cost"]
                rx_n = reaction_data["n"]
                for _ in range(cost):
                    logging.debug(f"Making recursive request for {rx_n} {precursor}.")
                    self.minimum_ore_for_chemical(precursor, rx_n, top_level=False)

        if not top_level:
            return

        self.ore_requests.sort(key=lambda x: x[3])
        logging.debug(f"ORE request for {n} {chemical}: {self.ore_requests}")

        # Now withdraw from ORE reserve, largest ORE withdrawal first
        #
        # check for A:
        #   not enough, react:
        #     A: output +10: (now [1B, 7A, 7A, 7A, 7A])
        #     A: reserve = 3 (now [1B, 7A, 7A, 7A])
        # check for A:
        #   not enough, react:
        #     A: output +10: (now [1B, 7A, 7A, 7A])
        #     A: reserve = 6 (now [1B, 7A, 7A])
        # check for A:
        #   not enough, react:
        #     A: output +10: (now [1B, 7A, 7A])
        #     A: reserve = 9 (now [1B, 7A])
        # check for A:
        #   enough:
        #     A: output +10: (now [1B, 7A])
        #     A: reserve = 2 (now [1B])
        # check for B:
        #   not enough, react:
        #     A: output +10: (now [1B, 7A, 7A])
        #     A: reserve = 9 (now [1B, 7A])

        ore_spent = 0

        while self.ore_requests:
            (chemical, n, cost, n_created) = self.ore_requests.pop()
            #  Get the current chemical reserve.  If it's not enough, react
            #  until there are enough.
            while self.g.nodes[chemical]["reserve"] < n:
                ore_spent += cost
                self.g.nodes[chemical]["reserve"] += n_created

            self.g.nodes[chemical]["reserve"] -= n

        return ore_spent

    @cached_property
    def minimum_ore(self):
        return self.minimum_ore_for_chemical("FUEL", 1)
