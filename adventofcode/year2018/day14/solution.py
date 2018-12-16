import itertools
import logging
import math

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

    def preceding(self, target, max_iterations=math.inf):
        target_length = len(target)

        for i in itertools.count():
            if i > max_iterations:
                break

            count = self.make_new_recipes()

            test_targets = [''.join(map(str, self.scores[-target_length:]))]
            if count == 2:
                test_targets.append(''.join(
                    map(str, self.scores[-target_length - 1:-1])))

            for j in range(len(test_targets)):
                if target == test_targets[j]:
                    return len(self.scores) - target_length - j

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

        return 2 if tens else 1


if __name__ == '__main__':
    target_string = get_data(year=2018, day=14)
    n = int(target_string)
    print("Problem 1:", RecipeScoreboard().ten_after(n))
    print("Problem 2:", RecipeScoreboard().preceding(target_string))
