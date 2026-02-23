from itertools import pairwise, count
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


def is_edge(s):
    return s in [RED, GREEN]


def is_inside(s):
    return s in [RED, GREEN, YELLOW]


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


class Turn(Enum):
    CONCAVE = 1
    CONVEX = 2


def go(point: tuple[int, int], direction: Heading) -> tuple[int, int]:
    x, y = point
    dx, dy = direction.value
    return (x + dx, y + dy)


def points_outside_turn(
    at: tuple[int, int], from_heading: Heading, to_heading: Heading
):
    # since we're turning 90 degrees, these spots are probably outside:
    # - directly ahead
    # - left and right of directly ahead
    # - opposite of new direction
    return {
        go(at, from_heading),
        go(at, from_heading.cw()),
        go(at, from_heading.ccw()),
        go(at, to_heading.opp()),
    }


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


def corner(head: Heading, current: tuple[int, int], next: tuple[int, int]) -> Turn:
    # Clockwise perspective, would this direction turn create a concave or convex corner
    match head, heading(current, next):
        case (
            (Heading.N, Heading.E)
            | (Heading.E, Heading.S)
            | (Heading.S, Heading.W)
            | (Heading.W, Heading.N)
        ):
            return Turn.CONVEX

        case (
            (Heading.N, Heading.W)
            | (Heading.W, Heading.S)
            | (Heading.S, Heading.E)
            | (Heading.E, Heading.N)
        ):
            return Turn.CONCAVE

        case _:
            # shouldn't be reachable as long as current and next headings are perpendicular
            return Turn.CONVEX


# def label_points(tile: tuple[int, int], head: Heading, turn: Turn):


def find_outside_border(red_tiles):
    outside = set()
    from_heading = heading(red_tiles[-1], red_tiles[0])
    out_pointer = heading(red_tiles[0], red_tiles[1]).opp()
    for start, end in pairwise(red_tiles + [red_tiles[0]]):
        # for start, end in pairwise(red_tiles[:2]):
        to_heading = heading(start, end)
        # print("start:", start)
        # print("end:", end)
        # print("from_heading:", from_heading)
        # print("to_heading:", to_heading)
        # print("out_pointer:", out_pointer)
        if to_heading == from_heading.cw().cw():
            # print("90deg")
            # +90deg turn: outside is 1) continuing old heading, 2) opposite of new heading, 3) between those
            outside.add(go(start, out_pointer))
            out_pointer = out_pointer.cw()
            outside.add(go(start, out_pointer))
            out_pointer = out_pointer.cw()
            outside.add(go(start, out_pointer))
        else:
            # print("-90deg")
            # -90deg turn: outside is between old and new
            out_pointer = out_pointer.ccw()
            outside.add(go(start, out_pointer))
            out_pointer = out_pointer.ccw()

        for point in get_path(start, end)[1:]:
            outside.add(go(point, out_pointer))

        from_heading = to_heading

    return outside


def evaluate_grid(red_tiles):
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


def difference(a, b):
    return 1 + abs(a - b)


def part1(red_tiles):
    combinations = [(a, b) for i, a in enumerate(red_tiles) for b in red_tiles[:i]]
    areas = [
        difference(x1, x2) * difference(y1, y2) for ((x1, y1), (x2, y2)) in combinations
    ]
    return max(areas)


def get_area(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    return difference(x1, x2) * difference(y1, y2)


def part2(red_tiles):
    outside_border = find_outside_border(red_tiles)

    if utils.input_type() == "example":
        # pretty print
        xs = [x for (x, _) in outside_border]
        ys = [y for (_, y) in outside_border]
        tiles = [[BLACK] * (max(xs) + 1) for _ in range(max(ys) + 1)]
        for x, y in outside_border:
            tiles[y][x] = BLUE
        # for x, y in red_tiles:
        #     tiles[y][x] = RED
        for (x1, y1), end in pairwise(red_tiles + [red_tiles[0]]):
            tiles[y1][x1] = RED
            for x2, y2 in get_path((x1, y1), end)[1:]:
                tiles[y2][x2] = GREEN
        print("\n".join(map("".join, tiles)))

    combinations = [(a, b) for i, a in enumerate(red_tiles) for b in red_tiles[:i]]
    areas = sorted([(get_area(a, b), a, b) for (a, b) in combinations], reverse=True)[
        4400:
    ]

    print(f"{len(outside_border)} points in outside border")
    print(f"{len(areas)} areas to check")
    counter = count()

    for area, a, b in areas:
        c = next(counter)
        if c > 1 and c % 10 == 0:
            print(f"Checked {c} areas. Most recent: {area}")

        if outside_inside(outside_border, a, b):
            continue

        return area

    return 0


def outside_inside(outside_border, a, b):
    for p in outside_border:
        if point_in_area(p, a, b):
            return True
    return False


def point_in_area(p, a, b):
    (x, y) = p
    (x1, y1), (x2, y2) = a, b
    x_in = x1 >= x >= x2 if x1 > x2 else x1 <= x <= x2
    y_in = y1 >= y >= y2 if y1 > y2 else y1 <= y <= y2
    return x_in and y_in


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    red_tiles = [tuple(map(int, line.split(","))) for line in puzzle_input]

    # the real grid is almost 10,000 x 10,000
    if utils.input_type() == "example":
        tiles = evaluate_grid(red_tiles)
        print("\n".join(map("".join, tiles)))

    # print("Part 1:", part1(red_tiles))

    pairs = pairwise(red_tiles + [red_tiles[0]])
    print("steps:", sum([len(get_path(a, b)) for a, b in pairs]))

    print("Part 2:", part2(red_tiles))
