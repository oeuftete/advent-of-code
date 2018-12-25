import logging
import pytest

from adventofcode.year2018.day23.solution import BotSpace


@pytest.fixture
def sample_bot_space():
    return BotSpace('''
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
'''.strip())


@pytest.mark.parametrize("i,signal,x,y,z", [
    (0, 4, 0, 0, 0),
    (6, 1, 1, 1, 1),
])
def test_parsed_bot(sample_bot_space, i, signal, x, y, z):
    bot = sample_bot_space.bots[i]
    assert bot.signal == signal
    assert bot.x == x
    assert bot.y == y
    assert bot.z == z
    assert bot.manhattan_distance(bot) == 0


@pytest.mark.parametrize("i,distance,in_range", [
    (0, 0, True),
    (1, 1, True),
    (2, 4, True),
    (3, 2, True),
    (4, 5, False),
    (5, 3, True),
    (6, 3, True),
    (7, 4, True),
    (8, 5, False),
])
def test_parsed_bot_space(sample_bot_space, i, distance, in_range):
    assert len(sample_bot_space.bots) == 9
    strongest = sample_bot_space.strongest_bot
    logging.debug(f'Strongest = {strongest}')

    distance_to_strongest = (
        sample_bot_space.bots[i].manhattan_distance(strongest))
    assert distance_to_strongest == distance
    assert (distance_to_strongest <= strongest.signal) == in_range
    assert len(sample_bot_space.bots_in_range) == 7


@pytest.fixture
def sample_bot_space_part_2():
    return BotSpace('''
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
'''.strip())


@pytest.mark.skip(reason='Way too slow')
def test_bot_in_range(sample_bot_space_part_2):
    assert sample_bot_space_part_2.signal_extent == \
        ((-150, -150, -150), (250, 250, 250))
    assert sample_bot_space_part_2.most_in_range_distance == 36
