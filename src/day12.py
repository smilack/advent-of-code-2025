from lark import Lark, Transformer
import utils


# I don't know if this is what this is supposed to look like, but it *does* work
class PuzzleTree(Transformer):
    NUM = int

    def start(self, start):
        return {"presents": start[0], "regions": start[1]}

    presents = dict
    present = tuple

    def shape(self, shape):
        return [[c == "#" for c in row] for row in shape]

    regions = list
    region = tuple
    dimensions = tuple
    required = list


if __name__ == "__main__":
    puzzle_input = utils.read_raw()

    parser = Lark.open("parse12.lark", rel_to=__file__, parser="earley")

    tree = PuzzleTree().transform(parser.parse(puzzle_input))

    print(tree["presents"])

    print(tree["regions"])

    print("Part 1:")

    print("Part 2:")
