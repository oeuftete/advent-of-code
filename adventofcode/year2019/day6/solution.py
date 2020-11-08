import networkx as nx


class OrbitMap(object):
    def __init__(self, input_map):
        self.g = nx.DiGraph()
        self.ORIGIN = 'COM'

        if isinstance(input_map, str):
            input_map = input_map.split('\n')
        self.input_map = input_map

        self._build_graph()

    def _build_graph(self):
        for orbit in self.input_map:
            (orbited, orbiter) = orbit.split(')')
            self.g.add_edge(orbited, orbiter)

    def has_orbit(self, orbiter, orbited):
        return nx.has_path(self.g, orbited, orbiter)

    def has_indirect_orbit(self, orbiter, orbited):
        return (self.has_orbit(orbiter, orbited)
                and not self.has_direct_orbit(orbiter, orbited))

    def has_direct_orbit(self, orbiter, orbited):
        return self.g.has_predecessor(orbiter, orbited)

    def n_total_orbits(self, orbiter):
        all_paths = nx.all_simple_paths(self.g, self.ORIGIN, orbiter)
        try:
            return len(next(all_paths)) - 1
        except StopIteration:
            return 0

    def n_indirect_orbits(self, orbiter):
        total = self.n_total_orbits(orbiter)
        return (total - 1) if total > 0 else 0

    def n_direct_orbits(self, orbiter):
        return 1 if self.n_total_orbits(orbiter) else 0

    def orbital_transfers(self, orbiter_one, orbiter_two):
        return max(
            0,
            nx.shortest_path_length(self.g.to_undirected(), orbiter_one,
                                    orbiter_two) - 2)

    @property
    def n_all_orbits(self):
        total = 0
        for n in self.g.nodes:
            total += self.n_total_orbits(n)
        return total
