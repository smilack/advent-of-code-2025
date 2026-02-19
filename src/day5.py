import utils

from functools import reduce


def make_range(s):
    low, high = map(int, s.split("-"))
    return range(low, high + 1)


def count_fresh(available: list[int], ranges):
    return sum([any([id in range_ for range_ in ranges]) for id in available])


def combine_sets(a: set[int], b: range) -> set[int]:
    return a.union(set(b))


def get_all_fresh(ranges):
    return reduce(combine_sets, ranges[1:], set(ranges[0]))


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    fresh_ranges = [make_range(s) for s in puzzle_input if "-" in s]
    available_ids = [int(s) for s in puzzle_input if s.isnumeric()]

    print("Part 1:", count_fresh(available_ids, fresh_ranges))

    print("Part 2:", len(get_all_fresh(fresh_ranges)))
