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
    def rendered(self):
        #  Make a new one-layer image, all '2's
        rendered_image = Image('2' * self.width * self.height,
                               (self.width, self.height))

        for l in self.layers:
            new_layer = Layer()
            for i, row in enumerate(l.rows):
                new_row = map(lambda x, y: y if x == '2' else x,
                              rendered_image.layers[0].rows[i], row)
                new_layer.append_row(new_row)

            rendered_image.layers = [new_layer]

        return '\n'.join([''.join(r) for r in rendered_image.layers[0].rows])

    @property
    def rendered_clearly(self):
        return self.rendered.translate(str.maketrans("10", u"\u2588 "))

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
