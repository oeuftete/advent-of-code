from aocd.models import Puzzle


def fuel_requirement(m):
    """Return the fuel requirement for one mass."""
    return int(m / 3) - 2


def fuel_requirements(masses):
    """Return the fuel requirements for a list of masses."""
    return sum(map(fuel_requirement, masses))


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=1)
    masses = map(int, puzzle.input_data.split('\n'))
    puzzle.answer_a = fuel_requirements(masses)
