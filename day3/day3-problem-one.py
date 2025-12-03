PUZZLE_INPUT_PATH = "../../puzzle-inputs/day3"

def get_largest_digit_index(battery: str):
    """Return the index of the first largest number we find"""
    largest_digit_index = 0
    largest_digit = 0
    for i in range(0, len(battery)):
        if int(battery[i]) > largest_digit:
            largest_digit_index = i
            largest_digit = int(battery[i])
            # Can return early since there's no larger digit than 9.
            if largest_digit == 9:
                return largest_digit_index
    return largest_digit_index


def get_largest_two_digit_number_indices(battery: str):
    # For the first digit: pass in a string which doesn't include the final character
    # otherwise we may not be able to create a two-digit number.
    largest_index = get_largest_digit_index(battery[0:len(battery)-1])
    # For the second digit, search from the next digit until the end.
    s_largest_index = get_largest_digit_index(
        battery[largest_index+1:]
    ) + largest_index + 1
    return largest_index, s_largest_index

def get_largest_problem_one_number(battery: str):
    # largest and second largest digit indices
    largest_index, s_largest_index = get_largest_two_digit_number_indices(battery)
    return (
        int(battery[largest_index]) * 10
    ) + int(battery[s_largest_index])


def get_batteries():
    with open(PUZZLE_INPUT_PATH) as file:
        for line in file.readlines():
            next_line = line.strip()
            if next_line != "":
                yield next_line


def main():
    sum = 0
    for battery in get_batteries():
        sum += get_largest_problem_one_number(battery)
    print(sum)

if __name__ == "__main__":
    main()
