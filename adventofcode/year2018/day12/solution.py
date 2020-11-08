import logging
import re
from collections import defaultdict

from aocd import get_data
from bitarray import bitarray


class PotRow:
    def __init__(self, rules):
        (self.initial, self.rule_set) = self.parse_rules(rules)
        self.bits = bitarray(self._to_bitarray(self.initial))
        self.origin = 0

    def _to_bitarray(self, s):
        return s.replace(".", "0").replace("#", "1")

    def _from_bitarray(self, s):
        return s.replace("0", ".").replace("1", "#")

    @property
    def state(self):
        return self._from_bitarray(self.bits.to01())

    def parse_rules(self, s):
        lines = s.split("\n")

        #  Get the initial state line
        INITIAL_FORMAT = re.compile(r"initial state: ([.#]+)")
        m_initial = re.match(INITIAL_FORMAT, lines[0])
        (initial_state,) = m_initial.groups()

        #  Skip the blank line
        #  Parse each rule: .##.# => #
        rules = defaultdict(lambda: ".")
        RULE_FORMAT = re.compile(r"([.#]{5}) => ([.#])")
        for l in lines[2:]:
            m_rules = re.match(RULE_FORMAT, l)
            (pattern, result) = m_rules.groups()
            rules[pattern] = result

        return (initial_state, rules)

    def generate(self, n=1):
        for _ in range(n):
            # pad each side, add to origin
            for _ in range(3):
                self.bits.insert(0, False)
                self.bits.append(False)
                self.origin += 1

            new_bits = self.bits.copy()

            # for each frame of 5, determine next gen, add to new result
            logging.debug("Input state: {}".format(self.state))
            for i in range(len(self.bits) - 5 + 1):
                pot_rule = self._from_bitarray(self.bits[i : i + 5].to01())
                pot_value = self.rule_set[pot_rule]
                logging.debug(
                    "Matched rule {} => {} at {}".format(pot_rule, pot_value, i)
                )
                new_bits[i + 2] = True if pot_value == "#" else False

            self.bits = new_bits

        # Optional for now
        # trim to max '....' on each side, adjusting origin if necessary

        return self

    @property
    def score(self):
        score = 0
        copy = self.bits.copy()

        logging.debug("bits = {}".format(self.bits))
        logging.debug("Copy = {}".format(copy))

        for i in range(len(copy)):
            if copy.pop(0):
                to_add = i - self.origin
                logging.debug("Found pot at index {}.  Adding {}.".format(i, to_add))
                score += to_add

        return score


if __name__ == "__main__":
    rules = get_data(year=2018, day=12)
    print("Problem 1:", PotRow(rules).generate(20).score)

    row = PotRow(rules)
    print("Problem 2:")
    last = 0
    for i in range(250):
        score = row.generate().score
        print("%6d: %6d (%4d)" % (i + 1, score, score - last))
        last = score
