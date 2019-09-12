import pytest

from adventofcode.year2018.day2.solution import (
    box_checksum,
    box_id_counter,
    common_letters_for_close,
)

SIMILAR_BOXES = ['abcde', 'fghij', 'klmno', 'pqrst', 'fguij', 'axcye', 'wvxyz']


@pytest.mark.parametrize("box_ids,matched_letters", [
    (SIMILAR_BOXES, 'fgij'),
])
def test_common_letters_for_close(box_ids, matched_letters):
    assert common_letters_for_close(box_ids) == matched_letters


@pytest.mark.parametrize("box_id,has_double,has_triple", [
    ('abcdef', False, False),
    ('bababc', True, True),
    ('abbcde', True, False),
    ('abcccd', False, True),
    ('aabcdd', True, False),
    ('abcdee', True, False),
    ('ababab', False, True),
])
def test_box_id_counter(box_id, has_double, has_triple):
    assert box_id_counter(box_id, 2) == has_double
    assert box_id_counter(box_id, 3) == has_triple


SAMPLE_BOXES = [
    'abcdef', 'bababc', 'abbcde', 'abcccd', 'aabcdd', 'abcdee', 'ababab'
]


@pytest.mark.parametrize("box_ids,checksum", [
    (SAMPLE_BOXES, 12),
])
def test_box_checksum(box_ids, checksum):
    assert box_checksum(box_ids) == checksum
