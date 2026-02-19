import utils


def maximum_joltage(bank):
    """Find the largest two digit number that can be created by picking two characters (in order) from a string of numbers.

    For example:
    - 98 in 987654321111111
    - 89 in 811111111111119
    - 78 in 234234234234278
    - 92 in 818181911112111

    Two cases:
    - Largest number is last digit
    - Largest number is any other digit
    """

    largest = largest_digit(bank)
    index = bank.index(largest)

    if index == len(bank) - 1:
        second = largest_digit(bank[:-1])
        return int(second + largest)
    else:
        second = largest_digit(bank[index + 1 :])
        return int(largest + second)


def largest_digit(s):
    return max(set(s))


if __name__ == "__main__":
    battery_banks = utils.read_lines()

    joltages = map(maximum_joltage, battery_banks)
    print("Part 1:", sum(joltages))

    print("Part 2:")
