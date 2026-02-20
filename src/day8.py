import utils
import numpy as np


def connections():
    if utils.input_type() == "example":
        return 10
    elif utils.input_type() == "real":
        return 1000
    else:
        return 0


def print_points(points):
    [print(f"({x}, {y}, {z})") for (x, y, z) in points]


def distance(a: np.ndarray, b: np.ndarray):
    return np.linalg.norm(a - b)


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    points = [np.fromstring(s, sep=",") for s in puzzle_input]
    print_points(points)
    print(distance(points[0], points[1]))

    distances = [
        (distance(points[i], points[j]), points[i], points[j])
        for i in range(len(points))
        for j in range(i)
    ]
    distances.sort()
    print(len(distances))

    print("Part 1:")

    print("Part 2:")
