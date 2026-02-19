from utils import read_csv
from sys import argv


def to_range(s):
    low, high = s.split("-")
    return range(int(low), int(high) + 1)


def repeats_once(i):
    mid = len(i) // 2
    return i[mid:] == i[:mid]


def all_equal(strs):
    """Determine if all strings in a list are equal."""
    return len(set(strs)) == 1


def groups_of(string, length):
    """Split a string into substrings of given length."""
    return [string[i : i + length] for i in range(0, len(string), length)]


def is_invalid(id):
    lengths = repeat_lengths[len(id)]
    for length in lengths:
        if all_equal(groups_of(id, length)):
            return True
    return False


repeat_lengths = {
    0: [],
    1: [],
    2: [1],
    3: [1],
    4: [1, 2],
    5: [1],
    6: [1, 2, 3],
    7: [1],
    8: [1, 2, 4],
    9: [1, 3],
    10: [1, 2, 5],
}

if __name__ == "__main__":
    if len(argv) < 2:
        print("Not enough arguments. Please provide input file name.")
        raise SystemExit
    else:
        input_name = argv[1]

    try:
        puzzle_input = read_csv(2, input_name)
    except FileNotFoundError:
        raise SystemExit

    # Part 1
    ranges = [to_range(s) for s in puzzle_input]
    invalid = [x for range_ in ranges for x in range_ if repeats_once(str(x))]
    print(sum(invalid))

    # Part 2
    invalid2 = [x for range_ in ranges for x in range_ if is_invalid(str(x))]
    # print(invalid2)
    print(sum(invalid2))
