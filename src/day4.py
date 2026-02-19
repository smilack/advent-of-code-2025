import utils


def adjacent(matrix, r, c):
    cells = []
    for r_ in [r - 1, r, r + 1]:
        for c_ in [c - 1, c, c + 1]:
            if 0 <= r_ < len(matrix):
                if 0 <= c_ < len(matrix[r_]):
                    if r_ != r or c_ != c:
                        cells.append(matrix[r_][c_])
    return cells


def adjacent2(matrix, r, c):
    return [
        matrix[r_][c_]
        for r_ in [r - 1, r, r + 1]
        for c_ in [c - 1, c, c + 1]
        if 0 <= r_ < len(matrix) and 0 <= c_ < len(matrix[r_]) and (r_ != r or c_ != c)
    ]


def valid_roll(matrix, r, c):
    return matrix[r][c] == "@" and adjacent(matrix, r, c).count("@") < 4


def part1(matrix):
    return [
        valid_roll(matrix, r, c)
        for r in range(len(matrix))
        for c in range(len(matrix[r]))
    ].count(True)


def flatten(matrix):
    return "".join(map("".join, matrix))


def remove_rolls(matrix) -> tuple[list[list[str]], int]:
    initial_rolls = flatten(matrix).count("@")

    new_matrix = [
        [
            "." if valid_roll(matrix, r, c) else matrix[r][c]
            for c in range(len(matrix[r]))
        ]
        for r in range(len(matrix))
    ]

    final_rolls = flatten(new_matrix).count("@")
    return (new_matrix, initial_rolls - final_rolls)


def part2(matrix):
    total_removed = 0
    matrix, removed = remove_rolls(matrix)

    while removed > 0:
        total_removed += removed
        matrix, removed = remove_rolls(matrix)

    return matrix, total_removed


if __name__ == "__main__":
    puzzle_input = utils.read_matrix()

    print("Part 1:", part1(puzzle_input))
    # print("\n".join(map("".join, puzzle_input)))

    new_matrix, removed = part2(puzzle_input)
    print("Part 2:", removed)
    # print("\n".join(map("".join, new_matrix)))
