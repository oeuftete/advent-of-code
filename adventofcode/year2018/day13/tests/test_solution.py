import pytest
from adventofcode.year2018.day13.solution import Cart, Track


@pytest.fixture
def sample_track():
    SAMPLE_TRACK = r'''
/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/
    '''.strip()
    return Track(SAMPLE_TRACK)


@pytest.fixture
def cleanup_track():
    CLEANUP_TRACK = r'''
/>-<\
|   |
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
    '''.strip()
    t = Track(CLEANUP_TRACK)
    t.crash_ends = False
    return t


def test_initial_track(sample_track):
    assert sample_track.grid_square(0, 0) == '/'
    assert sample_track.grid_square(1, 0) == '-'
    assert sample_track.grid_square(2, 0) == '-'  # starts with a cart on it
    assert sample_track.grid_square(12, 0) == ' '
    assert sample_track.grid_square(9, 3) == '|'  # starts with a cart on it
    assert sample_track.grid_square(0, 1) == '|'
    assert sample_track.grid_square(12, 5) == ' '

    assert len(sample_track.carts) == 2

    assert sorted(sample_track.cart_positions) == [(2, 0), (9, 3)]
    assert sorted(sample_track.cart_vectors) == [Cart.DOWN, Cart.RIGHT]


def test_moves(sample_track):
    sample_track.iterate()
    assert sorted(sample_track.cart_positions) == [(3, 0), (9, 4)]
    assert sorted(sample_track.cart_vectors) == [Cart.RIGHT, Cart.RIGHT]

    sample_track.iterate()
    assert sorted(sample_track.cart_positions) == [(4, 0), (10, 4)]
    assert sorted(sample_track.cart_vectors) == [Cart.DOWN, Cart.RIGHT]


def test_crash(sample_track):
    sample_track.run()
    assert sample_track.collision_position == (7, 3)
    assert sample_track.iterations == 14


def test_cleanup(cleanup_track):
    cleanup_track.run()
    assert len(cleanup_track.carts) == 1
    assert cleanup_track.carts[0].position == (6, 4)
