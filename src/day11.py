from functools import cache
from re import findall
import utils
from itertools import count

counter = count()


def parse_device(s):
    matches = findall("[a-z]{3}", s)
    return (matches[0], matches[1:])


def find_paths(devices, device, path=[], depth=1, visits=[]):
    if depth > len(devices):
        print("Potential cycle detected:", path)

    if device == "out":
        if all([v in path for v in visits]):
            print(f"{next(counter)} Valid path at depth", depth)
            # print(path)
            return 1
        else:
            print(f"{next(counter)} Invalid path at depth", depth)
            return 0
    else:
        return sum(
            [
                find_paths(devices, d, path + [d], depth + 1, visits)
                for d in devices[device]
            ]
        )


@cache
def find_paths_good(device, passed_fft=False, passed_dac=False):
    if device == "out":
        if passed_dac and passed_fft:
            return 1
        else:
            return 0
    else:
        return sum(
            [
                find_paths_good(d, passed_fft or d == "fft", passed_dac or d == "dac")
                for d in devices[device]
            ]
        )


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    global devices
    devices = dict([parse_device(line) for line in puzzle_input])
    # print(devices)

    if utils.input_type() in ["example", "real"]:
        paths = find_paths(devices, "you")
        print("Part 1:", paths)

    if utils.input_type() in ["example2", "real"]:
        # paths2 = find_paths(devices, "svr", visits=["fft", "dac"])
        paths2 = find_paths_good("svr")
        print("Part 2:", paths2)
