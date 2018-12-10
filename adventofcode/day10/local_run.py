#!/usr/bin/env python

import itertools
import logging
import os
import sys

from aocd import get_data

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from adventofcode.day10.solution import (  # noqa: E402
    data_to_sky
)

from adventofcode.day10.tests.resources import (  # noqa: E402
    get_test_data,
)


TEST_POINTS = get_test_data()


logging.basicConfig(level=logging.INFO)


print(data_to_sky(TEST_POINTS).iterate(3).dump_sky())

data = get_data(year=2018, day=10).split('\n')
problem_sky = data_to_sky(data)

for i in itertools.count():
    s = problem_sky.iterate().dump_sky(70, 10)
    if s:
        print("Iteration", i+1)  # 0 was the initial state
        print(s)
        break
