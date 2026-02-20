import utils


BLANK = " "
START = "╷"
SPLITTER = "△"
SPLIT = "🮧"
LEFT = "🮣"
RIGHT = "🮢"
BOTH = "🮦"
DOWN = "│"

input_symbols = {
    ".": BLANK,
    "S": START,
    "^": SPLITTER,
}


def drip_from(matrix: list[list[tuple[str, int]]], position: tuple[int, int]) -> int:
    (from_row, col) = position
    row = from_row + 1

    if row >= len(matrix):
        return 1

    symbol, count = matrix[row][col]

    if symbol == BLANK:
        child_count = drip_from(matrix, (row, col))
        matrix[row][col] = (DOWN, child_count)
        return child_count

    elif symbol == SPLITTER:
        left_symbol, left_children = matrix[row][col - 1]
        if left_symbol == BLANK:
            left_children = drip_from(matrix, (row, col - 1))
            matrix[row][col - 1] = (LEFT, left_children)

        right_symbol, right_children = matrix[row][col + 1]
        if right_symbol == BLANK:
            right_children = drip_from(matrix, (row, col + 1))
            matrix[row][col + 1] = (RIGHT, right_children)

        children = left_children + right_children
        matrix[row][col] = (SPLIT, children)
        return children

    elif symbol in [LEFT, RIGHT, BOTH, DOWN]:
        return count

    else:
        return 0


def print_matrix(m):
    top = "┌" + ("─" * len(m[0])) + "┐"
    bottom = "└" + ("─" * len(m[0])) + "┘"

    print(top)
    [print("│" + "".join([s for (s, _) in line]) + "│") for line in m]
    print(bottom)


if __name__ == "__main__":
    puzzle_input = [
        [(input_symbols[s], 0) for s in line] for line in utils.read_matrix()
    ]

    print_matrix(puzzle_input)

    start = (0, puzzle_input[0].index((START, 0)))
    timelines = drip_from(puzzle_input, start)

    print_matrix(puzzle_input)

    flattened = "".join(["".join([s for (s, _) in line]) for line in puzzle_input])

    print("Part 1:", flattened.count(SPLIT))

    print("Part 2:", timelines)
