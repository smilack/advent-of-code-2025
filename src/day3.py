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


def ultra_maximum_joltage(bank):
    """Find the largest two digit number that can be created by picking *twelve* characters (in order) from a string of numbers.

    For example:
    - 987654321111 in 987654321111111
    - 811111111119 in 811111111111119
    - 434234234278 in 234234234234278
    - 888911112111 in 818181911112111
    """

    while len(bank) > 12:
        for i in range(len(bank)):
            # Remove the first digit that is smaller than the following digit, or if there is none, remove the last digit
            if i == len(bank) - 1 or bank[i] < bank[i + 1]:
                bank = bank[:i] + bank[i + 1 :]
                break

    return int(bank)


if __name__ == "__main__":
    battery_banks = utils.read_lines()

    print("Part 1:", sum(map(maximum_joltage, battery_banks)))

    print("Part 2:", sum(map(ultra_maximum_joltage, battery_banks)))
