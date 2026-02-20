from typing import Any
from numpy._typing import NDArray
import numpy as np
from functools import reduce
from operator import mul
import utils


def connections():
    if utils.input_type() == "example":
        return 10
    elif utils.input_type() == "real":
        return 1000
    else:
        return 0


def print_points(points):
    [print(f"({x}, {y}, {z})") for (x, y, z) in points]


def distance(a: Point, b: Point) -> np.floating[Any]:
    return np.linalg.norm(a - b)


def find_distances(point: list[Point]) -> list[Pair]:
    """Return a list of (distance, point a, point b) for each pair of points.

    Sorted with the closest points at the end, for easy popping.
    """
    return sorted(
        [(distance(a, b), a, b) for i, a in enumerate(points) for b in points[:i]],
        reverse=True,
    )


def connect_circuits(remaining: int, circuits: list[Circuit], distances: list[Pair]):
    if remaining == 0:
        return

    # closest remaining pair
    _, a, b = distances.pop()
    new_circuit: Circuit = { a, b }

    for circuit in circuits:
        if


type Point = NDArray[np.floating[Any]]
type Pair = tuple[np.floating[Any], Point, Point]
type Circuit = set[Point]

if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    points: list[Point] = [np.fromstring(s, sep=",") for s in puzzle_input]
    distances = find_distances(points)

    circuits = []
    connect_circuits(connections(), circuits, distances)

    three_largest = sorted(circuits, key=len, reverse=True)[:3]
    product = reduce(mul, three_largest)

    print("Part 1:", product)

    # print("Part 2:")
