from aocd.models import Puzzle


def recursive_fuel_requirement(m):
    """Return the fuel requirement for one mass and its fuel."""
    if m <= 0:
        return 0

    new_fuel = fuel_requirement(m)
    return new_fuel + recursive_fuel_requirement(new_fuel)


def fuel_requirement(m):
    """Return the fuel requirement for one mass."""
    return max(0, int(m / 3) - 2)


def fuel_requirements(masses, include_fuel=False):
    """Return the fuel requirements for a list of masses."""
    if include_fuel:
        requirement_f = recursive_fuel_requirement
    else:
        requirement_f = fuel_requirement

    return sum(map(requirement_f, masses))


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=1)
    masses = [int(m) for m in puzzle.input_data.split('\n')]
    puzzle.answer_a = fuel_requirements(masses)
    puzzle.answer_b = fuel_requirements(masses, include_fuel=True)
