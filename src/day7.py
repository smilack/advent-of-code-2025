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


def drip_from(matrix: list[list[str]], position: tuple[int, int]):
    (from_row, col) = position
    row = from_row + 1

    if row >= len(matrix):
        return 1

    symbol = matrix[row][col]

    if symbol == BLANK or symbol == DOWN:
        matrix[row][col] = DOWN
        return drip_from(matrix, (row, col))

    elif symbol == SPLITTER or symbol == SPLIT:
        matrix[row][col] = SPLIT

        left = matrix[row][col - 1]
        if left == BLANK:
            matrix[row][col - 1] = LEFT
        elif left == RIGHT:
            matrix[row][col - 1] = BOTH

        right = matrix[row][col + 1]
        if right == BLANK:
            matrix[row][col + 1] = RIGHT
        elif right == LEFT:
            matrix[row][col + 1] = BOTH

        return drip_from(matrix, (row, col - 1)) + drip_from(matrix, (row, col + 1))

    else:
        return 0


def print_matrix(m):
    top = "┌" + ("─" * len(m[0])) + "┐"
    bottom = "└" + ("─" * len(m[0])) + "┘"

    print(top)
    [print("│" + "".join(line) + "│") for line in m]
    print(bottom)


if __name__ == "__main__":
    puzzle_input = [[input_symbols[s] for s in line] for line in utils.read_matrix()]

    print_matrix(puzzle_input)

    start = (0, puzzle_input[0].index(START))
    timelines = drip_from(puzzle_input, start)

    print_matrix(puzzle_input)

    flattened = "".join(["".join(line) for line in puzzle_input])

    print("Part 1:", flattened.count(SPLIT))

    print("Part 2:", timelines)
