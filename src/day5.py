import utils

from functools import reduce


def make_range(s):
    low, high = map(int, s.split("-"))
    return range(low, high + 1)


def combine_ranges(a, b):
    return set(a).union(set(b))


def get_fresh_ids(range_strings):
    ranges = map(make_range, range_strings)
    return reduce(combine_ranges, ranges)


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    fresh_ids = get_fresh_ids([s for s in puzzle_input if "-" in s])
    print(fresh_ids)

    available_ids = [int(s) for s in puzzle_input if s.isnumeric()]
    print(", ".join(map(str, available_ids)))

    print("Part 1:", sum([id in fresh_ids for id in available_ids]))

    print("Part 2:")
