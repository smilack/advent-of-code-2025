from utils import read_csv
from sys import argv

def to_range(s):
    low, high = s.split('-')
    return range(int(low), int(high) + 1)

def is_invalid(i):
    mid = len(i) // 2
    return i[mid:] == i[:mid]

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
    invalid = [x for rs in ranges for x in rs if is_invalid(str(x))]
    print(sum(invalid))

    # Part 2
