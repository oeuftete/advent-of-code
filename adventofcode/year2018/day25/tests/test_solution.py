import pytest

from adventofcode.year2018.day25.solution import NightSky, Star


def test_star():
    origin_star = Star(csv='0,0,0,0')
    assert origin_star.manhattan_distance(Star(csv='3,0,0,0')) == 3


@pytest.fixture
def sample_skies():
    return [
        '''
 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0
        ''',
        '''
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0
        ''',
        '''
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2
        ''',
        '''
1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2
        ''',
    ]


@pytest.mark.parametrize("i,n_stars,n_constellations", [
    (0, 8, 2),
    (1, 10, 4),
    (2, 10, 3),
    (3, 10, 8),
])
def test_sky(sample_skies, i, n_stars, n_constellations):
    night_sky = NightSky(sample_skies[i])
    assert len(night_sky.stars) == n_stars
    assert len(night_sky.constellations) == n_constellations
