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


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    red_tiles = [tuple(map(int, line.split(","))) for line in puzzle_input]

    # the real grid is almost 10,000 x 10,000
    if utils.input_type() == "example":
        draw_grid(red_tiles)

    print("Part 1:")
