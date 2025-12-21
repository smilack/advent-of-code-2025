from os import path, listdir

INPUT_DIR = path.join(path.dirname(path.dirname(path.abspath(__file__))), "input")

def read_input(day, name):
    try:
        directory = path.join(INPUT_DIR, str(day))
        file_path = path.join(directory, name)
        with open(file_path) as f:
            text = f.read()
        return text
    except FileNotFoundError:
        print(f"Could not find input \"{name}\" for day {day}.")
        
        if path.exists(directory):
            files = listdir(directory)
        else:
            files = []

        if len(files) == 0:
            print("No input options available for {day}.")
        else:
            print(f"Input options are:")
            for f in files:
                print("-", f)

        raise

def read_lines(day, name):
    text = read_input(day, name)
    return text.split()

def read_csv(day, name):
    text = read_input(day, name)
    return [v.strip() for v in text.split(",")]
