import logging

from aocd import get_data

logging.basicConfig(level=logging.INFO)


class RecipeScoreboard():
    def __init__(self):
        self.scores = [3, 7]
        self.pointers = [0, 1]

    def ten_after(self, n):
        while len(self.scores) < (n + 10):
            self.make_new_recipes()

        return ''.join(map(str, self.scores[n:n + 10]))

    def make_new_recipes(self):
        sum = 0
        for recipe in self.pointers:
            sum += self.scores[recipe]

        tens = sum // 10
        if tens:
            self.scores.append(tens)

        self.scores.append(sum % 10)

        for i in range(len(self.pointers)):
            current_pointer = self.pointers[i]
            self.pointers[i] += self.scores[current_pointer] + 1
            self.pointers[i] %= len(self.scores)


if __name__ == '__main__':
    n = int(get_data(year=2018, day=14))
    print("Problem 1:", RecipeScoreboard().ten_after(n))
    print("Problem 2:", "TBD")
