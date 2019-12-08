from collections import Counter
import math


class Layer(object):
    def __init__(self, rows=None):
        self.rows = rows or list()

    def __eq__(self, other):
        if len(self.rows) != len(other.rows):
            return False

        for i, r in enumerate(self.rows):
            if r != other.rows[i]:
                return False

        return True

    def append_row(self, row):
        self.rows.append(list(row))


class Image(object):
    def __init__(self, data, size):
        self.data = data
        self.width, self.height = size
        self._build_layers()

    def _build_layers(self):
        self.layers = list()
        data_string = self.data

        while data_string:
            layer = Layer()
            for _ in range(self.height):
                layer.append_row(data_string[:self.width])
                data_string = data_string[self.width:]

            self.layers.append(layer)

    @property
    def solution_a(self):
        solution = None
        min_zeroes = math.inf

        for l in self.layers:
            counter = Counter()
            for r in l.rows:
                counter.update(r)

            if counter['0'] < min_zeroes:
                min_zeroes = counter['0']
                solution = counter['1'] * counter['2']

        return solution
