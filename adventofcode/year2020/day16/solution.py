import logging
from dataclasses import dataclass, field
from typing import Tuple

from aocd.models import Puzzle

logging.basicConfig(level=logging.INFO)


@dataclass
class Ticket:
    ticket_values: list = field(default_factory=list)


@dataclass
class TicketValidator:
    boundary_rules: dict = field(default_factory=dict)

    def is_value_valid_for_rule(self, v, field_name):
        is_valid = False
        for boundary in self.boundary_rules[field_name]:
            logging.debug("... boundary=%s", boundary)
            if v in range(boundary[0], boundary[1]):
                logging.debug("... value=%s VALID", v)
                is_valid = True

        return is_valid

    def is_valid(self, ticket) -> Tuple[bool, list]:
        logging.debug("Checking %s for validity...", ticket)

        invalid_values = []
        for v in ticket.ticket_values:
            logging.debug("... value=%s", v)
            is_valid = False
            for rule_field_name in self.boundary_rules:
                logging.debug("... rule=%s", rule_field_name)
                if self.is_value_valid_for_rule(v, rule_field_name):
                    is_valid = True
                    break

            if not is_valid:
                logging.debug("... value=%s INVALID", v)
                invalid_values.append(v)

        return (not bool(invalid_values), invalid_values)


@dataclass
class TicketNotebook:
    notes: list = field(default_factory=list)
    nearby: list = field(default_factory=list)
    validator: TicketValidator = field(default_factory=TicketValidator)
    field_map: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        mode = 0
        rules = {}

        for line in self.notes:
            if not line:
                mode += 1
                continue

            if mode == 0:
                ticket_field, ranges = line.split(": ")
                boundaries = []
                for raw_range in ranges.split(" or "):
                    incl_start, incl_end = raw_range.split("-")
                    boundaries.append((int(incl_start), int(incl_end) + 1))
                rules[ticket_field] = boundaries

            if mode == 1:
                if line.startswith("your ticket"):
                    continue
                self.my_ticket = Ticket([int(n) for n in line.split(",")])

            if mode == 2:
                if line.startswith("nearby"):
                    continue
                self.nearby.append(Ticket([int(n) for n in line.split(",")]))

        self.validator = TicketValidator(rules)
        self._build_field_map()

    def _build_field_map(self):
        ticket_fields = list(self.validator.boundary_rules.keys())
        possible_fields = [ticket_fields[:] for _ in range(len(ticket_fields))]

        for valid_ticket in self.valid_nearby:
            for ti, value in enumerate(valid_ticket.ticket_values):
                for ticket_field in ticket_fields:
                    logging.debug(
                        "Checking if field [%s] can be valid for value [%s]...",
                        ticket_field,
                        value,
                    )
                    if not self.validator.is_value_valid_for_rule(value, ticket_field):
                        logging.debug("... field [%s] was INVALID ...", ticket_field)
                        logging.debug(
                            "... current possible fields: %s", possible_fields[ti]
                        )
                        if ticket_field in possible_fields[ti]:
                            possible_fields[ti].remove(ticket_field)
                            logging.debug("... removed [%s]", ticket_field)

        logging.debug("All possible fields: %s", possible_fields)
        while any(len(pf) > 1 for pf in possible_fields):

            #  First, find any fields that are the only possibility
            identified_fields = []
            for pf in filter(lambda pf: len(pf) == 1, possible_fields):
                identified_fields.append(pf[0])

            #  Then, remove those from any others
            for pfi, pf in enumerate(possible_fields):
                if len(pf) == 1:
                    continue
                for idf in identified_fields:
                    if idf in pf:
                        pf.remove(idf)
                possible_fields[pfi] = pf

        logging.debug("All possible fields after elimination: %s", possible_fields)
        for i, field_names in enumerate(possible_fields):
            assert len(field_names) == 1
            self.field_map[field_names[0]] = i

    def validate_nearby(self, n) -> bool:
        return self.validator.is_valid(self.nearby[n])[0]

    @property
    def valid_nearby(self):
        return list(filter(lambda nt: self.validator.is_valid(nt)[0], self.nearby))

    @property
    def nearby_error_rate(self) -> int:
        rate = 0
        for nt in self.nearby:
            rate += sum(self.validator.is_valid(nt)[1])
        return rate

    def field_no(self, field_name) -> int:
        return self.field_map[field_name]

    @property
    def departure_product(self) -> int:
        product = 1
        for field_name, field_value in self.field_map.items():
            if field_name.startswith("departure"):
                product *= self.my_ticket.ticket_values[field_value]

        return product


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=16)
    notes = puzzle.input_data.strip().splitlines()
    ticket_notebook = TicketNotebook(notes)
    puzzle.answer_a = ticket_notebook.nearby_error_rate
    puzzle.answer_b = ticket_notebook.departure_product
