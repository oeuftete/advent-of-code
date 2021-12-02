import pytest

from adventofcode.year2020.day16.solution import TicketNotebook


@pytest.fixture(name="example_notes")
def fixture_example_notes():
    return """
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
""".strip().splitlines()


@pytest.fixture(name="part_b_notes")
def fixture_part_b_notes():
    return """
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
""".strip().splitlines()


@pytest.mark.skip
def test_ticket_notebook(example_notes):
    ticket_notebook = TicketNotebook(example_notes)

    assert len(ticket_notebook.nearby) == 4

    assert ticket_notebook.validate_nearby(0)
    assert not ticket_notebook.validate_nearby(1)
    assert not ticket_notebook.validate_nearby(2)
    assert not ticket_notebook.validate_nearby(3)
    assert ticket_notebook.nearby_error_rate == 71


def test_part_b_notebook(part_b_notes):
    ticket_notebook = TicketNotebook(part_b_notes)

    assert len(ticket_notebook.nearby) == 3
    assert len(ticket_notebook.valid_nearby) == 3

    assert ticket_notebook.field_no("row") == 0
    assert ticket_notebook.field_no("class") == 1
    assert ticket_notebook.field_no("seat") == 2
