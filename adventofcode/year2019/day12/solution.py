import logging
import re
from collections import defaultdict


class Moon(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.dx = self.dy = self.dz = 0

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"


class LunarOrrery(object):
    def __init__(self, position_data):
        self.iterations = 0
        self._build_moons(position_data)

    def _build_moons(self, position_data):
        self.moons = list()

        POSITION_FORMAT = re.compile(r"<x=(.*?), y=(.*?), z=(.*?)>")
        for position in position_data.split("\n"):
            m_pos = re.match(POSITION_FORMAT, position)
            self.moons.append(Moon(*[int(p) for p in m_pos.groups()]))

        self.position_hashes = [self.hash_positions()]

    def hash_positions(self):
        t = tuple()
        for moon in self.moons:
            t += (moon.x, moon.y, moon.z)
            t += (moon.dx, moon.dy, moon.dz)
        logging.debug("State: {}".format(" ".join([("%4d" % i) for i in t])))
        return hash(t)

    def iterate(self, n=None, stop_on_equal=False):
        initial_iterations = self.iterations
        while n is None or self.iterations < (n + initial_iterations):
            if self.iterations % 10000 == 0:
                logging.info(f"At iteration {self.iterations}...")
            self.apply_gravity()
            self.apply_velocity()
            self.iterations += 1

            h = self.hash_positions()

            if stop_on_equal and h in self.position_hashes:
                for m in self.moons:
                    print(m)

                break

            self.position_hashes.append(h)

    def iterate_until_equal(self):
        self.iterate(stop_on_equal=True)

    def apply_gravity(self):
        changes = defaultdict(lambda: defaultdict(int))
        for i in range(len(self.moons) - 1):
            for j in range(i + 1, len(self.moons)):
                if self.moons[i].x > self.moons[j].x:
                    changes[i][0] += -1
                    changes[j][0] += 1
                elif self.moons[i].x < self.moons[j].x:
                    changes[i][0] += 1
                    changes[j][0] += -1

                if self.moons[i].y > self.moons[j].y:
                    changes[i][1] += -1
                    changes[j][1] += 1
                elif self.moons[i].y < self.moons[j].y:
                    changes[i][1] += 1
                    changes[j][1] += -1

                if self.moons[i].z > self.moons[j].z:
                    changes[i][2] += -1
                    changes[j][2] += 1
                elif self.moons[i].z < self.moons[j].z:
                    changes[i][2] += 1
                    changes[j][2] += -1

        for i in range(len(self.moons)):
            self.moons[i].dx += changes[i][0]
            self.moons[i].dy += changes[i][1]
            self.moons[i].dz += changes[i][2]

    def apply_velocity(self):
        for i in range(len(self.moons)):
            self.moons[i].x += self.moons[i].dx
            self.moons[i].y += self.moons[i].dy
            self.moons[i].z += self.moons[i].dz

    @property
    def total_energy(self):
        total = 0
        for m in self.moons:
            pot = abs(m.x) + abs(m.y) + abs(m.z)
            kin = abs(m.dx) + abs(m.dy) + abs(m.dz)
            total += pot * kin
        return total
