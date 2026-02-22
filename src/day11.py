from re import findall
import utils


def parse_device(s):
    matches = findall("[a-z]{3}", s)
    return (matches[0], matches[1:])


def find_paths(devices, device, path=[], depth=1):
    if depth > len(devices):
        print("Potential cycle detected:", path)

    if device == "out":
        # print(path)
        return 1
    else:
        return sum(
            [find_paths(devices, d, path + [d], depth + 1) for d in devices[device]]
        )


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    devices = dict([parse_device(line) for line in puzzle_input])
    # print(devices)

    paths = find_paths(devices, "you")

    print("Part 1:", paths)

    print("Part 2:")
