import utils

from functools import reduce


def make_range(s):
    low, high = map(int, s.split("-"))
    return range(low, high + 1)


def count_fresh(available: list[int] | range, ranges: list[range]):
    return sum([any([id in range_ for range_ in ranges]) for id in available])


def get_full_range(ranges):
    lowest = min([r.start for r in ranges])
    highest = max([r.stop for r in ranges])
    return range(lowest, highest)


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    fresh_ranges = [make_range(s) for s in puzzle_input if "-" in s]
    available_ids = [int(s) for s in puzzle_input if s.isnumeric()]

    print("Part 1:", count_fresh(available_ids, fresh_ranges))

    full_range = get_full_range(fresh_ranges)
    num_fresh = count_fresh(full_range, fresh_ranges)
    # print("Full range length:", len(full_range))
    # print("Number of ranges:", len(fresh_ranges))
    print("Part 2:", num_fresh)
