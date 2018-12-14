from adventofcode.day12.tests.fixtures import sample_rules
from adventofcode.day12.solution import (
    PotRow
)


def test_pot_row_initial():
    row = PotRow(sample_rules())
    assert row.initial == '#..#.#..##......###...###'
    assert row.origin == 0
    assert row.rule_set['.....'] == '.'
    assert row.rule_set['...##'] == '#'


def test_pot_row_generation():
    row = PotRow(sample_rules())

    row.generate()
    assert '..#...#....#.....#..#..#..#..' in row.state

    row.generate()
    assert '..##..##...##....#..#..#..##..' in row.state

    assert PotRow(sample_rules()).generate(20).score == 325
