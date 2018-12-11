import logging
import math


class PowerGrid:
    def __init__(self, serial, square_size=300):
        self.square_size = square_size

        self.serial = serial
        self._build_grid()

    def cell(self, x, y):
        return self.grid[x - 1][y - 1]

    def max_square(self, scope=3):
        max_result = (None, None, -math.inf)
        for ix in range(self.square_size - scope + 1):
            for iy in range(self.square_size - scope + 1):
                square_power = 0
                top_left = (ix + 1, iy + 1)
                for x in range(top_left[0], top_left[0] + scope):
                    for y in range(top_left[1], top_left[1] + scope):
                        square_power += self.cell(x, y)

                if square_power > max_result[2]:
                    max_result = (*top_left, square_power)

        return max_result

    #  TODO: Maybe a faster way to do this would be to cache square_power
    #  values, and if we find a cached one from a smaller square, just build
    #  the next power from that + the remaining strips.
    def max_any_square(self):
        max_result = (None, None, 0, -math.inf)
        for square_size in range(1, self.square_size):
            logging.debug('Checking square size %d...' % square_size)
            max_for_square = self.max_square(square_size)
            if max_for_square[2] > max_result[3]:
                logging.debug('New max: {}'.format(max_for_square))
                max_result = (max_for_square[0], max_for_square[1],  # x, y
                              square_size, max_for_square[2])

        return max_result

    def _build_grid(self):
        self.grid = list()
        for ix in range(self.square_size):
            self.grid.append(list())
            for iy in range(self.square_size):
                self.grid[ix].append(self._power_value(ix + 1, iy + 1))

    def _power_value(self, x, y):
        rack_id = x + 10
        power_level = rack_id * y
        power_level += self.serial
        power_level *= rack_id
        power_level = (abs(power_level) // 100) % 10
        power_level -= 5
        return power_level


logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    print("Problem 1:", PowerGrid(4455).max_square())
    print("Problem 2:", PowerGrid(4455).max_any_square())
