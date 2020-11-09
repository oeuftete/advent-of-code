import logging
import math
import re

import networkx as nx
from cached_property import cached_property


class Nanofactory(object):
    def __init__(self, input_reactions):
        if isinstance(input_reactions, str):
            input_reactions = input_reactions.split("\n")
        self.input_reactions = input_reactions

        self.g = nx.DiGraph()
        self._build_graph()

        self.ore_requests = []

    def _build_graph(self):
        self.g.add_node("ORE", reserve=math.inf)

        REACTION_FORMAT = re.compile(r"(.*?) => (.*)")
        REACTANT_FORMAT = re.compile(r"(\d+) (\w+)")
        for reaction in self.input_reactions:
            m_reactants = re.match(REACTION_FORMAT, reaction)
            inputs, output = m_reactants.groups()

            m_output = re.match(REACTANT_FORMAT, output)
            n_output, output_reactant = m_output.groups()

            self.g.add_node(output_reactant, n_output=int(n_output), reserve=0)

            for input_string in [s.strip() for s in inputs.split(",")]:
                m_input = re.match(REACTANT_FORMAT, input_string)
                n_input, input_reactant = m_input.groups()

                self.g.add_edge(
                    output_reactant,
                    input_reactant,
                    n_output=int(n_output),
                    n_input=int(n_input),
                )

    def reset(self):
        for n in self.g.nodes():
            self.g.nodes[n]["reserve"] = 0

    def minimum_ore_for_chemical(self, chemical="FUEL", n=1, depth=0):
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

        if depth == 0:
            logging.debug("## TOP LEVEL ##")

        logging.debug("(%s) Determining ORE requirement for %s %s", depth, n, chemical)
        logging.debug(self.g.edges([chemical], data=True))
        for _, precursor, reaction_data in self.g.edges([chemical], data=True):
            logging.debug(f"... precursor found: {precursor}: {reaction_data}")
            if precursor == "ORE":
                logging.debug(f"Adding ORE request for {n} {chemical}.")
                self.ore_requests.append(
                    (chemical, n, reaction_data["n_input"], reaction_data["n_output"])
                )
            else:
                n_input = reaction_data["n_input"]
                n_output = reaction_data["n_output"]

                #  How many requests do we need to make?  If the precursor is
                #  created in bigger chunks than we need, we also need to account
                #  for that.
                n_requests = math.ceil(n / n_output)
                logging.debug(
                    f"Making {n_requests} recursive requests for {n_input} {precursor}."
                )

                precursor_n_output = self.g.nodes[precursor]["n_output"]
                n_optimized_requests = math.ceil(
                    n_input * (n_requests / precursor_n_output)
                )
                if n_optimized_requests < n_requests:
                    logging.debug(
                        "... optimized to %s requests for %s %s.",
                        n_optimized_requests,
                        precursor_n_output,
                        precursor,
                    )
                    n_requests = n_optimized_requests
                    n_input = precursor_n_output

                for _ in range(n_requests):
                    self.minimum_ore_for_chemical(precursor, n_input, depth=depth + 1)

        if depth > 0:
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
            (chemical, n, n_input, n_output) = self.ore_requests.pop()
            #  Get the current chemical reserve.  If it's not enough, react
            #  until there are enough.
            logging.debug(
                f"Fulfilling ORE request for {n} {chemical}: "
                f"n_input: {n_input}, n_output: {n_output}"
            )

            while self.g.nodes[chemical]["reserve"] < n:
                logging.debug(
                    "%s reserve: %s", chemical, self.g.nodes[chemical]["reserve"]
                )
                ore_spent += n_input
                self.g.nodes[chemical]["reserve"] += n_output

            logging.debug("Ore mined: %s", ore_spent)
            logging.debug(
                "%s reserve after ORE: %s", chemical, self.g.nodes[chemical]["reserve"]
            )
            self.g.nodes[chemical]["reserve"] -= n
            logging.debug(
                "%s reserve after fulfillment: %s",
                chemical,
                self.g.nodes[chemical]["reserve"],
            )

        logging.debug("All reserves after fulfillment:")
        for n in self.g.nodes:
            logging.debug("  %-5s reserve: %s", n, self.g.nodes[n]["reserve"])

        return ore_spent

    @cached_property
    def minimum_ore(self):
        return self.minimum_ore_for_chemical("FUEL", 1)
