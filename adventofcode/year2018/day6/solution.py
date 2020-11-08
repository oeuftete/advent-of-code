import logging
import math
from collections import Counter, defaultdict

from aocd import get_data

from adventofcode.common.coordinate import Coordinate

logging.basicConfig(level=logging.INFO)


def get_boundaries(coordinates):
    by_x = sorted(coordinates, key=lambda c: c.x)
    by_y = sorted(coordinates, key=lambda c: c.y)
    return ((by_x[0].x, by_x[-1].x), (by_y[0].y, by_y[-1].y))


def get_bound_indices(coordinates):
    unbound = list()
    i = 0

    for c in coordinates:
        bounded = defaultdict(bool)
        for c_other in coordinates:
            logging.debug("Checking {} against {}...".format(c, c_other))
            if c == c_other:
                logging.debug("...identity: {} == {}".format(c, c_other))
                continue

            for d in ["west", "east", "north", "south"]:
                if c.is_bounded_by(c_other, d):
                    logging.debug("...{} bound to the {} by {}".format(c, d, c_other))
                    bounded[d] = True
                    continue

        if (
            bounded["west"]
            and bounded["east"]
            and bounded["north"]
            and bounded["south"]
        ):
            logging.debug("{} ({}) bound in all directions".format(c, i))
            unbound.append(i)
        else:
            logging.debug("{} ({}) not bound: {}".format(c, i, bounded))

        i += 1

    return unbound


def get_boundary_indices(coordinates):
    ((min_x, max_x), (min_y, max_y)) = get_boundaries(coordinates)
    found = list()

    i = 0
    for c in coordinates:
        if c.x == min_x or c.x == max_x or c.y == min_y or c.y == max_y:
            found.append(i)
        i += 1

    return found


def get_safe_coordinates(coordinates, threshold):
    ((min_x, max_x), (min_y, max_y)) = get_boundaries(coordinates)
    range_x = max_x - min_x
    range_y = max_y - min_y

    #  For each point within a wide range...
    safe = list()

    for x in range(min_x - int(range_x / 2), max_x + int(range_x / 2)):
        for y in range(min_y - int(range_y / 2), max_y + int(range_y / 2)):
            here = Coordinate(x=x, y=y)
            total_distance = 0
            for c in coordinates:
                total_distance += here.manhattan_distance(c)

            if total_distance < threshold:
                safe.append(here)

    return safe


def largest_area(coordinates):
    ((min_x, max_x), (min_y, max_y)) = get_boundaries(coordinates)
    range_x = max_x - min_x
    range_y = max_y - min_y

    winners = Counter()

    #  For each point within the boundary...
    for x in range(min_x - int(range_x / 2), max_x + int(range_x / 2)):
        for y in range(min_y - int(range_y / 2), max_y + int(range_y / 2)):

            logging.debug("Checking {}:{}...".format(x, y))

            target = Coordinate(x=x, y=y)
            min_length = math.inf
            leading_i = None

            i = 0
            for c in coordinates:
                distance = c.manhattan_distance(target)
                if distance == 0:
                    logging.debug("C {} {} won {}:{} (identity)!".format(i, c, x, y))
                    winners.update([i])
                    leading_i = None
                    break

                elif distance == min_length:
                    logging.debug("{}:{} was pushed by C {} {}.".format(x, y, i, c))
                    leading_i = None

                elif distance < min_length:
                    logging.debug(
                        "C {} {} took the lead at {}:{}...".format(i, c, x, y)
                    )
                    leading_i = i
                    min_length = distance

                i += 1

            if leading_i is not None:
                logging.debug(
                    "C {} won {}:{} (after full search)!".format(leading_i, x, y)
                )
                winners.update([leading_i])

    logging.debug(winners)

    bound_indices = get_bound_indices(coordinates)

    for w in winners.most_common():
        (winner_index, winner_count) = w

        logging.debug("Checking winner {}".format(winner_index))
        if winner_index in bound_indices:
            logging.debug(
                "Leader {} ({}) is not bound.  Wins!".format(winner_index, winner_count)
            )
            return winner_count

        logging.debug(
            "Leader {} ({}) was unbound...".format(winner_index, winner_count)
        )

    #    For each coordinate...
    #      Find it's distance to the target point...
    #         If it's:
    #           0: this coordinate wins this one, move on
    #           non-zero:
    #             is it equal to the current min?  If so, draw.  Move on
    #             is it lt the current min?  New leader, continue search
    #             Otherwise, implicitly gt, continue search
    #
    #  See who won the most, return the count of it's wins


if __name__ == "__main__":
    coordinates = list(
        map(lambda c: Coordinate(csv=c), get_data(year=2018, day=6).split("\n"))
    )
    print("Problem 1:", largest_area(coordinates))
    print("Problem 2:", len(get_safe_coordinates(coordinates, 10000)))
