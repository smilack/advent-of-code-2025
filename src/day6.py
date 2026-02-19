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


if __name__ == "__main__":
    puzzle_input = utils.read_table()

    problems = np.transpose(puzzle_input)

    solutions = [solve_problem(p) for p in problems]

    print("Part 1:", sum(solutions))

    print("Part 2:")
