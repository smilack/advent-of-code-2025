from os import path, listdir
from sys import argv
import re

INPUT_DIR = path.join(path.dirname(path.dirname(path.abspath(__file__))), "input")


def input_type():
    try:
        return argv[1]
    except IndexError:
        return ""


def _read_input(day, name):
    directory = ""

    try:
        directory = path.join(INPUT_DIR, str(day))
        file_path = path.join(directory, name)
        with open(file_path) as f:
            text = f.read()
        return text
    except FileNotFoundError:
        print(f'Could not find input "{name}" for day {day}.')

        if path.exists(directory):
            files = listdir(directory)
        else:
            files = []

        if len(files) == 0:
            print("No input options available for {day}.")
        else:
            print("Input options are:")
            for f in files:
                print("-", f)

        raise SystemExit


def read_lines():
    return read_raw().rstrip("\n").split("\n")


def read_csv():
    return [v.strip() for v in read_raw().split(",")]


def read_matrix():
    """Split input into 2d array of single-character strings."""
    return [list(line) for line in read_lines()]


def read_table():
    """Split input into 2d array of whitespace-delimited values."""
    return [line.split() for line in read_raw().rstrip().split("\n")]


def read_raw():
    try:
        file_name = argv[0]
        input_name = argv[1]
    except IndexError:
        print("Not enough arguments. Please provide both script and input file names")
        raise SystemExit

    pattern = r"(?P<day>[\d]+)\.py"
    found = re.search(pattern, file_name)
    if found and found["day"]:
        day = found["day"]
    else:
        print("Could not determine puzzle day. Is it in the file name?")
        raise SystemExit

    return _read_input(day, input_name)
