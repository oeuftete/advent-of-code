def read_input(file_name):
    with open(file_name) as f:
        return list(map(lambda x: x.strip(), f.readlines()))
