from lark import Lark, Transformer
import utils


class PuzzleTree(Transformer):
    NUM = int

    # def full(self, _):
    #     return True

    # def empty(self, _):
    #     return False

    def row(self, row):
        return [x.data.value for x in row]

    # row = list
    shape = list
    present = tuple
    presents = dict

    dimensions = tuple

    def start(self, start):
        return {"presents": start[0], "regions": start[1]}

    required = list

    region = tuple

    regions = list


if __name__ == "__main__":
    puzzle_input = utils.read_raw()

    parser = Lark.open("parse12.lark", rel_to=__file__, parser="earley")

    tree = PuzzleTree().transform(parser.parse(puzzle_input))

    print(tree["presents"])

    print(tree["regions"])

    print("Part 1:")

    print("Part 2:")
