import itertools
from re import findall
import utils


class Machine:
    id_iter = itertools.count()

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

        print(f"Machine {self.id} activated with {depth} presses")

        return depth

    def __press(self, button, lights):
        return [light ^ b for (light, b) in zip(lights, button)]

    def jolt(self):
        results = self.buttons
        depth = 1

        while self.joltage_counters not in results:
            print(f"{len(results)} options tried with {depth} depth")
            depth += 1

            new_results = []

            # this at least tries to cut corners by checking each result as it's generated, but it still takes a ridiculous number of tries to find an answer
            # I don't know if a DFS with caching would work here
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


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    machines = [Machine(config) for config in puzzle_input]

    activation_presses = sum([machine.activate() for machine in machines])

    print("Part 1:", activation_presses)

    joltage_presses = sum([machine.jolt() for machine in machines])

    print("Part 2:", joltage_presses)
