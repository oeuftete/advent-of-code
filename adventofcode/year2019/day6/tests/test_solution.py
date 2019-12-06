from adventofcode.year2019.day6.solution import OrbitMap

TEST_MAP = '''
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
'''.strip()


def test_orbits():
    o = OrbitMap(TEST_MAP)

    assert o.n_direct_orbits('COM') == 0
    assert o.n_indirect_orbits('COM') == 0
    assert o.n_total_orbits('COM') == 0

    assert o.has_orbit('D', 'C')
    assert o.has_direct_orbit('D', 'C')
    assert o.has_indirect_orbit('D', 'B')
    assert o.has_indirect_orbit('D', 'COM')
    assert o.n_direct_orbits('D') == 1
    assert o.n_indirect_orbits('D') == 2
    assert o.n_total_orbits('D') == 3

    assert o.n_all_orbits == 42

    o.g.add_edge('K', 'YOU')
    o.g.add_edge('I', 'SAN')
    assert o.orbital_transfers('YOU', 'SAN') == 4
