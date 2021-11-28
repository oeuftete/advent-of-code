import attr
from aocd.models import Puzzle


@attr.s
class Captcha:
    raw = attr.ib()

    @property
    def solution(self):
        captcha_sum = 0
        last = self.raw[-1]
        for d in self.raw:
            if d == last:
                captcha_sum += int(d)
            last = d
        return captcha_sum

    @property
    def solution_two(self):
        captcha_sum = 0
        clen = len(self.raw)
        for i, d in enumerate(self.raw):
            if d == self.raw[int(i+clen/2) % clen]:
                captcha_sum += int(d)
        return captcha_sum


if __name__ == "__main__":
    puzzle = Puzzle(year=2017, day=1)
    captcha_string = puzzle.input_data.strip()
    puzzle.answer_a = Captcha(captcha_string).solution
    puzzle.answer_b = Captcha(captcha_string).solution_two
