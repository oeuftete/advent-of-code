import pytest

from adventofcode.year2017.day2.solution import Spreadsheet


@pytest.mark.parametrize(
    "row,expected",
    [
        ([5, 1, 9, 5], 8),
        ([7, 5, 3], 4),
        ([2, 4, 6, 8], 6),
    ],
)
def test_row_checksum(row, expected):
    assert Spreadsheet.row_checksum(row) == expected


@pytest.mark.parametrize(
    "row,expected",
    [
        ([5, 9, 2, 8], 4),
        ([9, 4, 7, 3], 3),
        ([3, 8, 6, 5], 2),
    ],
)
def test_row_division(row, expected):
    assert Spreadsheet.row_division(row) == expected


@pytest.mark.parametrize(
    "rows,expected",
    [
        (
            [
                [5, 1, 9, 5],
                [7, 5, 3],
                [2, 4, 6, 8],
            ],
            18,
        ),
        (
            [
                ["5", "1", "9", "5"],
                ["7", "5", "3"],
                ["2", "4", "6", "8"],
            ],
            18,
        ),
    ],
)
def test_spreadsheet_checksum(rows, expected):
    assert Spreadsheet(rows).checksum == expected


@pytest.mark.parametrize(
    "rows,expected",
    [
        (
            [
                [5, 9, 2, 8],
                [9, 4, 7, 3],
                [3, 8, 6, 5],
            ],
            9,
        )
    ],
)
def test_spreadsheet_division_checksum(rows, expected):
    assert Spreadsheet(rows).division_checksum == expected
