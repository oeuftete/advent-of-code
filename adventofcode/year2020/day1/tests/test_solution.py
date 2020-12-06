import pytest

from adventofcode.year2020.day1.solution import ExpenseReport


@pytest.fixture(name="simple_expenses")
def fixture_simple_expenses():
    return [1721, 979, 366, 299, 675, 1456]


@pytest.mark.parametrize("tuple_size,product", [(2, 514579), (3, 241861950)])
def test_product_2020(simple_expenses, tuple_size, product):
    assert ExpenseReport(simple_expenses, tuple_size=tuple_size).product_2020 == product


def test_bad_expense_list():
    expense_report = ExpenseReport([1, 2, 3])
    with pytest.raises(ValueError):
        _ = expense_report.product_2020
