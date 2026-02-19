from operator import add, mul
from functools import reduce
import numpy as np
import utils


operators = {"+": add, "*": mul}


def solve_problem(problem):
    """Perform an operation on a list of numbers where the operator is given as a string in the last item of the list.

    For example, solve_problem(["123", "45", "6", "*"]) == 33210.
    """
    operands = [int(n) for n in problem[:-1]]
    operator = operators[problem[-1]]
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
    transposed = np.transpose([number.split() for number in problem])
    converted = ["".join(line).strip() for line in transposed]
    return converted


def solve(problems):
    return sum(map(solve_problem, problems))


if __name__ == "__main__":
    # it turns out the vertical alignment matters, so I can't strip the whitespace this early
    puzzle_input = utils.read_table()

    problems = np.transpose(puzzle_input)

    print("Part 1:", solve(problems))

    part_2_problems = [transpose_numbers(p[:-1]) + [p[-1]] for p in problems]

    print("Part 2:", solve(part_2_problems))
