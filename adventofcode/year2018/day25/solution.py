from collections import Counter
import logging
import uuid

from aocd import get_data

logging.basicConfig(level=logging.INFO)


class Star():
    def __init__(self, **kwargs):
        if kwargs.get('csv', None):
            (self.x, self.y, self.z,
             self.t) = map(int, kwargs['csv'].replace(" ", "").split(","))
        else:
            self.x = kwargs['x']
            self.y = kwargs['y']
            self.z = kwargs['z']
            self.t = kwargs['t']

    def manhattan_distance(self, other):
        return (abs(self.x - other.x) + abs(self.y - other.y) +
                abs(self.z - other.z) + abs(self.t - other.t))

    def __str__(self):
        return "({}, {}, {}, {})".format(self.x, self.y, self.z, self.t)


class Constellation():
    def __init__(self):
        self.name = str(uuid.uuid4())
        self.stars = list()

    def add_star(self, s):
        self.stars.append(s)

    def merge(self, other):
        self.stars = list(set(self.stars) | set(other.stars))

    def __str__(self):
        return '{}: {}'.format(self.name, ', '.join(map(str, self.stars)))


class NightSky():
    def __init__(self, stardata):
        self.stars = list()
        for star_csv in stardata.strip().split('\n'):
            self.stars.append(Star(csv=star_csv))
        self.constellations = list()
        self.build_constellations()

    def build_constellations(self):
        for s in self.stars:
            is_added = False
            for c in self.constellations:
                for o in c.stars:
                    if s.manhattan_distance(o) <= 3:
                        c.add_star(s)
                        is_added = True
                        break

            if not is_added:
                new_c = Constellation()
                new_c.add_star(s)
                self.constellations.append(new_c)

        #  All stars are now part of one or more constellations.  Look for all
        #  stars part of multiple constellations, then merge those
        #  constellations together.
        last_count = -1
        while last_count != len(self.constellations):
            logging.debug('Constellations')
            for c in self.constellations:
                logging.debug('  {}'.format(c))
            last_count = len(self.constellations)
            logging.debug('Count was: {}...'.format(last_count))
            self.merge_constellations()
            logging.debug('New count is: {}...'.format(len(
                self.constellations)))

    def merge_constellations(self):
        star_counter = Counter([
            s for stars in map(lambda c: c.stars, self.constellations)
            for s in stars
        ])

        c_merged_to = dict()
        original_constellations = self.constellations

        for s in [s for s, s_count in star_counter.items() if s_count > 1]:

            #  Find the list of constellations to merge.
            c_to_merge = [c for c in original_constellations if s in c.stars]

            #  Use the first one as the constellation to keep and the rest as
            #  the targets to merge in.
            for c_target in c_to_merge[1:]:

                base_c = c_to_merge[0]
                logging.debug("[{}] merging in [{}]".format(
                    base_c.name, c_target.name))

                #  If our constellations aren't still in the constellation
                #  list, it must have been merged into another.  Find that one,
                #  and make that one the base constellation.
                while base_c not in self.constellations:
                    logging.debug("  base [{}] was gone...".format(
                        base_c.name))
                    base_c = c_merged_to[base_c]
                    logging.debug("  ... was merged to [{}]".format(
                        base_c.name))

                while c_target not in self.constellations:
                    logging.debug("  target [{}] was gone...".format(
                        c_target.name))
                    c_target = c_merged_to[c_target]
                    logging.debug("  ... was merged to [{}]".format(
                        c_target.name))

                if base_c != c_target:
                    base_c.merge(c_target)
                    c_merged_to[c_target] = base_c
                    self.constellations = [
                        c for c in self.constellations
                        if c != c_target and c.stars
                    ]


if __name__ == '__main__':
    data = get_data(year=2018, day=25)
    print("Problem 1:", len(NightSky(data).constellations))
    print("Problem 2:", "TBD")
