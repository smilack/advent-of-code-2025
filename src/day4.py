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


if __name__ == "__main__":
    puzzle_input = utils.read_matrix()

    print("Part 1:", part1(puzzle_input))
    # print("\n".join(map("".join, puzzle_input)))

    print("Part 2:")
