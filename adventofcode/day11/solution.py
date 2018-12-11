import math


class PowerGrid:
    def __init__(self, serial, x_size=300, y_size=300):
        self.x_size = x_size
        self.y_size = y_size

        self.serial = serial
        self._build_grid()

    def cell(self, x, y):
        return self.grid[x - 1][y - 1]

    def max_square(self, x_scope=3, y_scope=3):
        max_result = (None, None, -math.inf)
        for ix in range(self.x_size - x_scope + 1):
            for iy in range(self.y_size - x_scope + 1):
                square_power = 0
                top_left = (ix + 1, iy + 1)
                for x in range(top_left[0], top_left[0] + x_scope):
                    for y in range(top_left[1], top_left[1] + y_scope):
                        square_power += self.cell(x, y)

                if square_power > max_result[2]:
                    max_result = (*top_left, square_power)

        return max_result

    def _build_grid(self):
        self.grid = list()
        for ix in range(self.x_size):
            self.grid.append(list())
            for iy in range(self.y_size):
                self.grid[ix].append(self._power_value(ix + 1, iy + 1))

    def _power_value(self, x, y):
        rack_id = x + 10
        power_level = rack_id * y
        power_level += self.serial
        power_level *= rack_id
        power_level = (abs(power_level) // 100) % 10
        power_level -= 5
        return power_level


if __name__ == '__main__':
    print("Problem 1:", PowerGrid(4455).max_square())
    print("Problem 2:", "TBD")
