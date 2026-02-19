import sys
from functools import reduce

EXAMPLE = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""


def rotation_to_int(rotation: str) -> int:
    return int(rotation[1:]) * (1 if rotation[0] == "R" else -1)


def stops(turns: list[int]) -> list[int]:
    current = 50
    return [current := (current + n) % 100 for n in turns]


def stops_at_zero(turns: list[int]) -> int:
    return stops(turns).count(0)


def turns_through_zero(turns: list[int]) -> int:
    _, zeroes = reduce(rotate_through, turns, (50, 0))
    return zeroes


def rotate_through(acc: tuple[int, int], turn) -> tuple[int, int]:
    """Do rotation and count number of passes through zero."""
    current, zeroes = acc
    moved = current + turn

    # crossed 0
    if current > 0 and moved <= 0:
        zeroes += 1

    # crossed a multiple of 100
    zeroes = int(abs(moved) / 100)

    return (moved % 100, zeroes)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        with open(sys.argv[1]) as f:
            rotations = f.read()
    else:
        rotations = EXAMPLE

    turns = [rotation_to_int(s) for s in rotations.split()]

    print("Part one:", stops_at_zero(turns))
    print("Part two:", turns_through_zero(turns))
