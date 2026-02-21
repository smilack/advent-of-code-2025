import utils

GREEN = "🟩"
RED = "🟥"


def draw_grid(red_tiles):
    xs = [p[0] for p in red_tiles]
    ys = [p[1] for p in red_tiles]

    tiles = [[GREEN for _ in range(max(xs) + 1)] for _ in range(max(ys) + 1)]

    for x, y in red_tiles:
        tiles[y][x] = RED

    print("\n".join(map("".join, tiles)))


def difference(a, b):
    return 1 + abs(a - b)


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    red_tiles = [tuple(map(int, line.split(","))) for line in puzzle_input]

    # the real grid is almost 10,000 x 10,000
    if utils.input_type() == "example":
        draw_grid(red_tiles)

    combinations = [(a, b) for i, a in enumerate(red_tiles) for b in red_tiles[:i]]
    areas = [
        difference(x1, x2) * difference(y1, y2) for ((x1, y1), (x2, y2)) in combinations
    ]

    print("Part 1:", max(areas))
