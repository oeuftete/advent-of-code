from collections import Counter
import math


class Layer(object):
    def __init__(self, size, data):
        self.size = size

        assert len(data) == self.area
        self.data = data

        self.rows = list()

        self._build_layer()

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    @property
    def area(self):
        return self.width * self.height

    def _build_layer(self):
        data_string = self.data
        for _ in range(self.height):
            while data_string:
                self.append_row(data_string[: self.width])
                data_string = data_string[self.width :]

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
        self.size = size
        self.width, self.height = size
        self._build_layers()

    def _build_layers(self):
        self.layers = list()
        data_string = self.data

        for _ in range(self.area):
            while data_string:
                layer = Layer(size=self.size, data=data_string[: self.area])
                self.layers.append(layer)
                data_string = data_string[self.area :]

    @property
    def area(self):
        return self.width * self.height

    @property
    def rendered(self):
        #  Make a new layer, all transparent '2's
        new_layer = Layer(size=self.size, data="2" * self.area)

        for layer in self.layers:
            for i, row in enumerate(layer.rows):
                new_layer.rows[i] = list(
                    map(lambda x, y: y if x == "2" else x, new_layer.rows[i], row)
                )

        return "\n".join(["".join(r) for r in new_layer.rows])

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

            if counter["0"] < min_zeroes:
                min_zeroes = counter["0"]
                solution = counter["1"] * counter["2"]

        return solution
