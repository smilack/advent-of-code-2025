from typing import Iterable
from itertools import count, product, compress, chain, combinations
from functools import reduce
from operator import mul
from re import findall
from iterables import zip_sum, scale
import utils


class Machine:
    id_iter = count()

    def __init__(self, config):
        self.id = next(Machine.id_iter)

        # Example config: "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
        # lights are . or #
        self.lights: list[bool] = [
            True if c == "#" else False for c in findall("[.#]", config)
        ]

        # buttons are numbers in parens
        # this captures all numbers or commas in parens
        # don't have to bother with actual parsing like (\d+(,\d+)*) because we just split the result on commas anyway
        button_numbers: list[list[int]] = [
            [int(n) for n in s.split(",")] for s in findall(r"\(([\d,]+)\)", config)
        ]
        # then convert to bool array with same length as lights so pressing a button is just a zipped XOR
        self.buttons: list[list[bool]] = [
            [i in button for i in range(len(self.lights))] for button in button_numbers
        ]

        # joltage basically same as buttons but only one entry
        self.joltage_counters = [
            int(n) for n in findall(r"{([\d,]+)}", config)[0].split(",")
        ]

    def activate(self):
        results = self.buttons
        depth = 1

        while self.lights not in results:
            depth += 1
            # this is slow because it calculates all the results before checking if any is the answer
            results = [
                self.__press(button, result)
                for result in results
                for button in self.buttons
            ]

        # print(f"Machine {self.id} activated with {depth} presses")

        return depth

    def __press(self, button, lights):
        return [light ^ b for (light, b) in zip(lights, button)]

    def jolt(self):
        print("Machine", self.id, "joltages:\n")
        show_joltage_matrices(self.buttons, self.joltage_counters)

        # the upper bound for presses for a button is the lowest counter that the button affects
        button_maxima = [
            min(compress(self.joltage_counters, button)) for button in self.buttons
        ]

        # print(button_maxima)
        options = reduce(mul, button_maxima)

        eq_matrix = transpose(self.buttons)
        press_ranges = [range(m + 1) for m in button_maxima]
        best = button_maxima
        tested = 0

        power_eqs = filter(None, powerset(zip(eq_matrix, self.joltage_counters)))
        for eq_set in power_eqs:
            eqs, res = zip(*eq_set)
            tot_eq = zip_sum(*eqs)
            tot_re = sum(res)
            print(
                " ".join(
                    [f"{k}{letter(i)}" if k else "  " for i, k in enumerate(tot_eq)]
                ),
                "=",
                tot_re,
            )

        press_combinations = filter(
            press_filter(eq_matrix, self.joltage_counters, count()),
            product(*press_ranges),
        )
        for current in press_combinations:
            tested += 1
            if tested % 1_000_000 == 0:
                print(f"Tested {tested:,} / {options - tested:,}")

            if sum(current) >= sum(best):
                continue

            elif test(current, self.buttons, self.joltage_counters):
                best = current

        print(self.id, ":", sum(best))
        return sum(best)

    def jolt_bfs(self):
        results = self.buttons
        # lower bound: highest counter
        # return max(self.joltage_counters)
        depth = 1

        while self.joltage_counters not in results:
            print(f"{len(results)} options tried with {depth} depth")
            depth += 1

            new_results = []

            # this at least tries to cut corners by checking each result as it's generated, but it still takes a ridiculous number of tries to find an answer
            # I don't know if a DFS with caching would work here
            #
            # multiplication???
            # something, something, system of equations? matrix?
            #
            #     (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
            #
            #     A * [0, 0, 0, 1]
            #   + B * [0, 1, 0, 1]
            #   + C * [0, 0, 1, 0]
            #   + D * [0, 0, 1, 1]
            #   + E * [1, 0, 1, 0]
            #   + F * [1, 1, 0, 0]
            #   ------------------
            #   =     [3, 5, 4, 7]
            #
            #   0 <= k <= max(counter)
            #
            for r in results:
                for button in self.buttons:
                    new_result = self.__jolt_press(button, r)
                    if new_result == self.joltage_counters:
                        print(f"Machine {self.id} jolted with {depth} presses")
                        return depth

                    if all(
                        [
                            new_result[i] <= self.joltage_counters[i]
                            for i in range(len(r))
                        ]
                    ):
                        new_results.append(new_result)

            results = new_results

        return depth

    def __jolt_press(self, button, counters):
        # taking advantage of True/False implicit conversion to 1/0
        return [counter + b for (counter, b) in zip(counters, button)]


def add_eqns():
    pass


def powerset(iterable):
    # from https://docs.python.org/3/library/itertools.html
    "Subsequences of the iterable from shortest to longest."
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def test(
    presses: Iterable[int], buttons: list[list[bool]], targets: Iterable[int]
) -> bool:
    return targets == zip_sum(
        *[scale(k, button) for k, button in zip(presses, buttons)]
    )


def press_filter(equations, results, counter):
    total = satisfies_total(equations, results)
    equalities = satisfies_equalities(equations, results)

    def fil(press):
        c = next(counter)
        if c > 0 and c % 5_000_000 == 0:
            print(f"Filtered {c:,}")
        return total(press) and equalities(press)

    return fil


def satisfies_total(equations, results):
    total_eqn = zip_sum(*equations)
    total_result = sum(results)

    def calculate(press):
        lhs = sum([p * k for p, k in zip(press, total_eqn)])
        return lhs == total_result

    return calculate


def satisfies_equalities(equations, results):
    def check(presses):
        for equation, result in zip(equations, results):
            if sum(compress(presses, equation)) != result:
                return False
        return True

    return check


def show_joltage_matrices(buttons, joltage_counters):
    output = []

    number_length = max([len(str(n)) for n in joltage_counters])
    for i, button in enumerate(buttons):
        output.append(vector_to_str(i, button, number_length))

    output_width = len(output[-1])
    output.append("—" * output_width)

    # it's hacky but 'A' - 4 = '='
    output.append(vector_to_str(-4, joltage_counters, number_length))
    output.append("")

    eq_matrix = transpose(buttons)
    for i, (equation, joltage) in enumerate(zip(eq_matrix, joltage_counters)):
        output.append(equation_to_str(equation) + " = " + str(joltage))
    output.append("")

    total_eqn = zip_sum(*eq_matrix)
    total_result = sum(joltage_counters)
    output.append(
        " + ".join([f"{k}{letter(i)}" for i, k in enumerate(total_eqn)])
        + " = "
        + str(total_result)
    )

    for i, button in enumerate(buttons):
        counters = list(compress(joltage_counters, button))
        output.append(
            f"max({letter(i)}) = min({','.join(map(str, counters))}) = {min(counters)}"
        )

    print("\n".join(output), "\n")


def vector_to_str(index, vector, number_length):
    contents = " ".join([str(int(i)).rjust(number_length, " ") for i in vector])
    return f"{letter(index)} [ {contents} ]"


def equation_to_str(equation):
    return (
        "sum( "
        + " ".join([letter(i) if x else " " for i, x in enumerate(equation)])
        + " )"
    )


def letter(i: int):
    return chr(i + ord("A"))


def transpose(matrix: list[list]):
    return [[row[c] for row in matrix] for c in range(len(matrix[0]))]


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    machines = [Machine(config) for config in puzzle_input]

    # activation_presses = sum([machine.activate() for machine in machines])

    # print("Part 1:", activation_presses)

    joltage_presses = sum([machine.jolt() for machine in machines][:1])

    print("Part 2:", joltage_presses)
