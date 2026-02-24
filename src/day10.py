from itertools import count, product
from functools import reduce
from operator import mul
from re import findall
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
        # print("Machine", self.id, "joltages:\n")
        # show_joltage_matrices(self.buttons, self.joltage_counters)

        button_maxima = [
            min([self.joltage_counters[i] for i in range(len(button)) if button[i]])
            for button in self.buttons
        ]

        print(button_maxima)
        options = reduce(mul, button_maxima)

        press_ranges = [range(m + 1) for m in button_maxima]
        best = button_maxima
        tested = 0
        for current in product(*press_ranges):
            tested += 1
            if tested % 100000 == 0:
                print(f"Tested {tested:,} / {options - tested:,}")
            if sum(current) >= sum(best):
                continue
            elif test(current, self.buttons, self.joltage_counters):
                best = current

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


def zip_sum(*args: list[int]) -> list[int]:
    return list(map(sum, zip(*args)))


def scale(k: int, lst: list[bool]) -> list[int]:
    return [k * x for x in lst]


def test(
    presses: tuple[int, ...], buttons: list[list[bool]], targets: list[int]
) -> bool:
    return targets == zip_sum(
        *[scale(k, button) for k, button in zip(presses, buttons)]
    )


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
    eq_joltages = transpose([joltage_counters])
    for i, (equation, joltage) in enumerate(zip(eq_matrix, eq_joltages)):
        output.append(equation_to_str(equation) + " = " + str(joltage[0]))
    output.append("")

    for i, button in enumerate(buttons):
        counters = [joltage_counters[j] for j in range(len(button)) if button[j]]
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

    joltage_presses = sum([machine.jolt() for machine in machines])

    print("Part 2:", joltage_presses)
