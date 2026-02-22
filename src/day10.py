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

    def activate(self):
        results = self.buttons
        depth = 1

        while self.lights not in results:
            depth += 1
            results = [
                self.__press(button, result)
                for result in results
                for button in self.buttons
            ]

        print(f"Machine {self.id} activated with {depth} presses")

        return depth

    def __press(self, button, lights):
        return [light ^ b for (light, b) in zip(lights, button)]


if __name__ == "__main__":
    puzzle_input = utils.read_lines()

    presses = sum([Machine(config).activate() for config in puzzle_input])
    print("Part 1:", presses)

    print("Part 2:")
