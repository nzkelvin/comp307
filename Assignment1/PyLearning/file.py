def read_data_file(path):
    try:
        with open(path, "r") as data_file:
            # readlines() is optional here
            for line in data_file.readlines():
                yield line
    except Exception:
        print("Could not read file")


def load_data_from_file(path):
    data_lines = read_data_file(path)
    for data_line in data_lines:
        yield data_line.split()
