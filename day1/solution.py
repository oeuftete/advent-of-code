from functools import reduce
import os


def read_input(file_name):
    with open(file_name) as f:
        content = map(lambda x: x.strip(), f.readlines())

    return list(content)


def frequency_summer(frequency_list):
    return reduce(lambda x, y: x + y, map(int, frequency_list))


if __name__ == '__main__':
    print(frequency_summer(read_input(
        os.path.join(os.path.dirname(os.path.realpath(__file__)),
                     '..', 'input/input-day1-1.txt')
    )))
