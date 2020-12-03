import pytest

from adventofcode.year2020.day1.solution import ExpenseReport


@pytest.fixture
def simple_expense_report():
    return ExpenseReport([1721, 979, 366, 299, 675, 1456])


def test_product_2020(simple_expense_report):
    assert simple_expense_report.product_2020 == 514579
