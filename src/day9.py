from itertools import pairwise, cycle
import utils

BLACK = "⬛"
BLUE = "🟦"
GREEN = "🟩"
RED = "🟥"
YELLOW = "🟨"


def steps(a, b):
    if a == b:
        return [a]
    else:
        return range(a, b, (b - a) // abs(b - a))


def repeating_zip(a, b):
    if len(a) > len(b):
        return zip(a, cycle(b))
    elif len(b) > len(a):
        return zip(cycle(a), b)
    else:
        return zip(a, b)


def get_path(a, b):
    (x1, y1), (x2, y2) = a, b
    return list(repeating_zip(steps(x1, x2), steps(y1, y2)))


def is_edge(s):
    return s in [RED, GREEN]


def is_inside(s):
    return s in [RED, GREEN, YELLOW]


def evaluate_grid(red_tiles):
    xs = [p[0] for p in red_tiles]
    ys = [p[1] for p in red_tiles]

    tiles = [[BLACK for _ in range(max(xs) + 1)] for _ in range(max(ys) + 1)]

    for (x1, y1), end in pairwise(red_tiles + [red_tiles[0]]):
        tiles[y1][x1] = RED
        for x2, y2 in get_path((x1, y1), end)[1:]:
            tiles[y2][x2] = GREEN

    for line in tiles:
        inside = False
        on_edge = False
        for i in range(len(line)):
            if is_edge(line[i]):
                on_edge = True
            else:
                if on_edge:
                    on_edge = False
                    inside = not inside

                if inside:
                    line[i] = YELLOW

    return tiles


def difference(a, b):
    return 1 + abs(a - b)


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    red_tiles = [tuple(map(int, line.split(","))) for line in puzzle_input]

    tiles = evaluate_grid(red_tiles)

    # the real grid is almost 10,000 x 10,000
    if utils.input_type() == "example":
        print("\n".join(map("".join, tiles)))

    combinations = [(a, b) for i, a in enumerate(red_tiles) for b in red_tiles[:i]]
    areas = [
        difference(x1, x2) * difference(y1, y2) for ((x1, y1), (x2, y2)) in combinations
    ]

    print("Part 1:", max(areas))
