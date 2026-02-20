from operator import add, mul
from functools import reduce
import numpy as np
import re
import utils


operators = {"+": add, "*": mul}


def solve_problem(problem):
    """Perform an operation on a list of numbers where the operator is given as a string in the last item of the list.

    For example, solve_problem(["123", "45", "6", "*"]) == 33210.
    """
    operands = [int(n.strip()) for n in problem[:-1]]
    operator = operators[problem[-1].strip()]
    return reduce(operator, operands)


def transpose_numbers(problem):
    """Transpose the digits of a list of numbers.

    For example:
        123
         45
          6
        ["123", "45", "6"] becomes ["356", "24", "1"]

        328
        64
        98
        ["328", "64", "98"] becomes ["8", "248", "369"]
    """
    transposed = np.transpose([list(number) for number in problem])
    converted = ["".join(line).strip() for line in transposed]
    return converted


def solve(problems):
    return sum(map(solve_problem, problems))


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    # The operator is always aligned with the left column:
    # 123 328  51 64
    #  45 64  387 23
    #   6 98  215 314
    # *   +   *   +
    # abcdefghijklmnop

    # [a, e, i, m]
    operator_places = [
        match.start() for match in re.finditer(r"\*|\+", puzzle_input[-1])
    ]

    # [(a, e-1), (e, i-1), (i, m-1)]
    # [(a, d), (e, h), (i, l)]
    column_bounds = [
        (operator_places[i - 1], operator_places[i] - 1)
        for i in range(1, len(operator_places))
    ]
    # (m, p)
    column_bounds.append((operator_places[-1], len(puzzle_input[-1])))

    columns = [
        [line[start:stop] for (start, stop) in column_bounds] for line in puzzle_input
    ]

    problems = np.transpose(columns)
    print("Part 1:", solve(problems))

    part_2_problems = [transpose_numbers(p[:-1]) + [p[-1]] for p in problems]
    print("Part 2:", solve(part_2_problems))
