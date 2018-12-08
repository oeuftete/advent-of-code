import pytest

from adventofcode.day8.solution import (
    sum_all_metadata
)


TEST_TREE_DATA = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
#                 A----------------------------------
#                     B----------- C-----------
#                                      D-----


@pytest.mark.parametrize("tree_data,metadata_sum", [
    (TEST_TREE_DATA, 138),
])
def test_sum_all_metadata(tree_data, metadata_sum):
    assert sum_all_metadata(tree_data) == metadata_sum
