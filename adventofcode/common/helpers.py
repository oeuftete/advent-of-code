import os


def read_input(file_name):
    with open(file_name) as f:
        return list(map(lambda x: x.strip(), f.readlines()))


def day_data(day):
    return read_input(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '..', '..', 'input/input-day{}.txt'.format(day)
        )
    )
