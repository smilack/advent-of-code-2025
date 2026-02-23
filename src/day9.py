from itertools import pairwise
from enum import Enum
import utils

BLACK = "⬛"
BLUE = "🟦"
GREEN = "🟩"
RED = "🟥"
YELLOW = "🟨"


def steps(a, b):
    if a < b:
        return range(a, b, 1)
    elif a > b:
        return range(a, b, -1)
    else:
        return [a]


def get_path(a, b):
    (x1, y1), (x2, y2) = a, b
    x_steps = steps(x1, x2)
    y_steps = steps(y1, y2)
    if isinstance(x_steps, list) and len(x_steps) == 1:
        path = zip(x_steps * len(y_steps), y_steps)
    elif isinstance(y_steps, list) and len(y_steps) == 1:
        path = zip(x_steps, y_steps * len(x_steps))
    else:
        path = zip(x_steps, y_steps)
    return list(path)


class Heading(Enum):
    N = (0, -1)
    NE = (1, -1)
    E = (1, 0)
    SE = (1, 1)
    S = (0, 1)
    SW = (-1, 1)
    W = (-1, 0)
    NW = (-1, -1)

    def cw(self):
        return self.__go(1)

    def ccw(self):
        return self.__go(-1)

    def __go(self, next_or_prev):
        values = list(self.__class__)
        index = values.index(self)
        return values[(index + next_or_prev) % len(values)]

    def opp(self):
        return self.__go(4)


def go(point: tuple[int, int], direction: Heading) -> tuple[int, int]:
    x, y = point
    dx, dy = direction.value
    return (x + dx, y + dy)


def heading(old: tuple[int, int], new: tuple[int, int]) -> Heading:
    (x1, y1), (x2, y2) = old, new
    # It's assumed that x1 == x2 XOR y1 == y2
    if x1 == x2:
        if y2 > y1:
            return Heading.S
        else:
            return Heading.N
    else:
        if x2 > x1:
            return Heading.E
        else:
            return Heading.W


def find_outside_border(red_tiles):
    outside = set()
    from_heading = heading(red_tiles[-1], red_tiles[0])
    out_pointer = heading(red_tiles[0], red_tiles[1]).opp()
    for start, end in pairwise(red_tiles + [red_tiles[0]]):
        to_heading = heading(start, end)
        if to_heading == from_heading.cw().cw():
            # +90deg turn: outside is 1) continuing old heading, 2) opposite of new heading, 3) between those
            outside.add(go(start, out_pointer))
            out_pointer = out_pointer.cw()
            outside.add(go(start, out_pointer))
            out_pointer = out_pointer.cw()
            outside.add(go(start, out_pointer))
        else:
            # -90deg turn: outside is between old and new
            out_pointer = out_pointer.ccw()
            outside.add(go(start, out_pointer))
            out_pointer = out_pointer.ccw()

        for point in get_path(start, end)[1:]:
            outside.add(go(point, out_pointer))

        from_heading = to_heading

    return outside


def part1(red_tiles):
    tile_combinations = [(a, b) for i, a in enumerate(red_tiles) for b in red_tiles[:i]]
    areas = [get_area(a, b) for a, b in tile_combinations]
    return max(areas)


def difference(a, b):
    return 1 + abs(a - b)


def get_area(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    return difference(x1, x2) * difference(y1, y2)


def part2(red_tiles):
    outside_border = find_outside_border(red_tiles)

    if utils.input_type() == "example":
        draw_outside_border(red_tiles, outside_border)

    combinations = [(a, b) for i, a in enumerate(red_tiles) for b in red_tiles[:i]]
    areas = sorted([(get_area(a, b), a, b) for (a, b) in combinations], reverse=True)

    for area, a, b in areas:
        if outside_is_inside(outside_border, a, b):
            continue

        return area

    return 0


def outside_is_inside(outside_border, corner1, corner2):
    for point in outside_border:
        if point_in_area(point, corner1, corner2):
            return True
    return False


def point_in_area(point, corner1, corner2):
    (x, y) = point
    (x1, y1), (x2, y2) = corner1, corner2
    x_in = x1 >= x >= x2 if x1 > x2 else x1 <= x <= x2
    y_in = y1 >= y >= y2 if y1 > y2 else y1 <= y <= y2
    return x_in and y_in


def draw_outside_border(red_tiles, outside_border):
    xs = [x for (x, _) in outside_border]
    ys = [y for (_, y) in outside_border]
    tiles = [[BLACK] * (max(xs) + 1) for _ in range(max(ys) + 1)]
    for x, y in outside_border:
        tiles[y][x] = BLUE
    for (x1, y1), end in pairwise(red_tiles + [red_tiles[0]]):
        tiles[y1][x1] = RED
        for x2, y2 in get_path((x1, y1), end)[1:]:
            tiles[y2][x2] = GREEN
    print("\n".join(map("".join, tiles)))


def draw_grid(red_tiles):
    xs = [p[0] for p in red_tiles]
    ys = [p[1] for p in red_tiles]

    tiles = [[BLACK] * (max(xs) + 1) for _ in range(max(ys) + 1)]

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


def is_edge(s):
    return s in [RED, GREEN]


def is_inside(s):
    return s in [RED, GREEN, YELLOW]


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    red_tiles = [tuple(map(int, line.split(","))) for line in puzzle_input]

    # the real grid is almost 10,000 x 10,000
    if utils.input_type() == "example":
        tiles = draw_grid(red_tiles)
        print("\n".join(map("".join, tiles)))

    print("Part 1:", part1(red_tiles))

    print("Part 2:", part2(red_tiles))
