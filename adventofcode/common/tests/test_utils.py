from adventofcode.common.utils import list_str_to_int


def test_list_str_to_int():
    assert list_str_to_int(["1", "0", "47"]) == [1, 0, 47]
