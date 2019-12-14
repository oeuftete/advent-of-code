from adventofcode.year2019.day12.solution import LunarOrrery

TEST_INITIAL_POSITIONS = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
""".strip()


def test_lunar_orrery():
    orrery = LunarOrrery(TEST_INITIAL_POSITIONS)

    assert orrery.moons[0].dx == 0
    assert orrery.moons[0].x == -1

    orrery.iterate(1)
    assert orrery.iterations == 1
    assert orrery.moons[0].x == 2
    assert orrery.moons[0].dx == 3

    orrery.iterate(9)
    assert orrery.iterations == 10
    assert orrery.moons[0].x == 2
    assert orrery.moons[0].dx == -3

    assert orrery.total_energy == 179

    orrery.iterate_until_equal()
    assert orrery.iterations == 2772
