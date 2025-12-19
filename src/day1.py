import sys

def toInt(s):
    return int(s[1:]) * (1 if s[0] == 'R' else -1)

def runningTotal(l):
    current = 50
    return [current := (current + n) % 100 for n in l]

def part1(turns):
    totals = runningTotal(turns)
    return totals.count(0)

def part2(turns):
    return 0

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        with open(sys.argv[1]) as f:
            puzzleInput = f.read()
    else:
        puzzleInput = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

    turns = [toInt(s) for s in puzzleInput.split()]

    print("Part one:", part1(turns)) 
    print("Part two:", part2(turns))
