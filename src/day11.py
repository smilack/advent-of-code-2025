from functools import cache
from re import findall
import utils


def parse_device(s):
    matches = findall("[a-z]{3}", s)
    return (matches[0], matches[1:])


def find_paths(devices, device, path=[], depth=1):
    if depth > len(devices):
        print("Potential cycle detected:", path)

    if device == "out":
        return 1
    else:
        return sum(
            [find_paths(devices, d, path + [d], depth + 1) for d in devices[device]]
        )


@cache
# By not including the devices dict, all the arguments (str, bool, bool) are hashable, so the result can be cached
def find_paths_hashable(device, passed_fft=False, passed_dac=False):
    if device == "out":
        if passed_dac and passed_fft:
            return 1
        else:
            return 0
    else:
        return sum(
            [
                find_paths_hashable(
                    d, passed_fft or d == "fft", passed_dac or d == "dac"
                )
                for d in devices[device]
            ]
        )


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    devices = dict([parse_device(line) for line in puzzle_input])

    if utils.input_type() in ["example", "real"]:
        print("Part 1:", find_paths(devices, "you"))

    if utils.input_type() in ["example2", "real"]:
        print("Part 2:", find_paths_hashable("svr"))
