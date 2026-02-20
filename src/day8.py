from math import sqrt
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


def distance(a: Point, b: Point):
    return sqrt(sum([(i - j) ** 2 for i, j in zip(a, b)]))


def find_distances(points: list[Point]) -> list[Pair]:
    """Return a list of (distance, point a, point b) for each pair of points.

    Sorted with the closest points at the end, for easy popping.
    """
    return sorted(
        [(distance(a, b), a, b) for i, a in enumerate(points) for b in points[:i]],
        reverse=True,
    )


def connect_circuits(circuits: list[Circuit], distances: list[Pair]):
    # closest remaining pair
    _, a, b = distances.pop()
    new_circuit: Circuit = {a, b}

    # check overlap with existing circuits
    added_to = []
    for circuit in circuits:
        if not circuit.isdisjoint(new_circuit):
            circuit |= new_circuit
            added_to.append(circuit)

    # add to list
    if not added_to:
        circuits.append(new_circuit)
    # or add to & consolidate existing circuits
    else:
        for c in added_to[1:]:
            added_to[0] |= c
            circuits.remove(c)


type Point = tuple[int, ...]
type Pair = tuple[float, Point, Point]
type Circuit = set[Point]


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    points: list[Point] = [tuple(map(int, line.split(","))) for line in puzzle_input]

    distances = find_distances(points)

    circuits = []
    for _ in range(connections()):
        connect_circuits(circuits, distances)

    three_largest = sorted(map(len, circuits), reverse=True)[:3]
    product = reduce(mul, three_largest)

    print("Part 1:", product)

    # print("Part 2:")
