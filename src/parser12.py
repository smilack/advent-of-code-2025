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


def get_input():
    puzzle_input = utils.read_raw()
    parser = Lark.open("parse12.lark", rel_to=__file__, parser="earley")
    return PuzzleTree().transform(parser.parse(puzzle_input))
