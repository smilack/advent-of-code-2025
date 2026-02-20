import utils


def print_points(points):
    [print(f"({x}, {y}, {z})") for (x, y, z) in points]


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    points = [tuple([int(n) for n in s.split(",")]) for s in puzzle_input]
    print_points(points)

    print("Part 1:")

    print("Part 2:")
