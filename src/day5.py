import utils


def make_range(s):
    low, high = map(int, s.split("-"))
    return range(low, high + 1)


def count_fresh(available: list[int] | range, ranges: list[range]):
    return sum([any([id in range_ for range_ in ranges]) for id in available])


def get_full_range(ranges):
    lowest = min([r.start for r in ranges])
    highest = max([r.stop for r in ranges])
    return range(lowest, highest)


def add_range(ranges, new_range):
    """Add a range to a list of ranges, merging it into an existing range if possible.

    ranges is assumed to be sorted and new_range must sort >= ranges[-1].
    """
    if len(ranges) == 0:
        ranges.append(new_range)
    else:
        ranges.extend(merge_ranges(ranges.pop(), new_range))


def sort_ranges(ranges):
    with_metadata = [(r.start, r.stop, i, r) for (i, r) in enumerate(ranges)]
    with_metadata.sort()
    return [range_ for (_, _, _, range_) in with_metadata]


def merge_ranges(a: range, b: range) -> list[range]:
    """Combine two ranges, if possible, otherwise leave separate. Return a list
    of either one or two ranges.

    a is assumed to be sorted before b (sorting by min asc, max asc).

    |---a---|
    |---b---|

    |---a---|
    |---b------|

    |---a---|
       |---b---|

    |-----a-----|
      |---b---|
    """
    if b.start in a:
        return [range(a.start, max(a.stop, b.stop))]
    else:
        return [a, b]


def merge_all_ranges(sorted_ranges):
    merged_ranges = []
    for r in sorted_ranges:
        add_range(merged_ranges, r)
    return merged_ranges


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    fresh_ranges = [make_range(s) for s in puzzle_input if "-" in s]
    available_ids = [int(s) for s in puzzle_input if s.isnumeric()]

    print("Part 1:", count_fresh(available_ids, fresh_ranges))

    sorted = sort_ranges(fresh_ranges)
    super_range = merge_all_ranges(sorted)
    total_fresh = sum([len(range_) for range_ in super_range])
    print("Part 2:", total_fresh)
