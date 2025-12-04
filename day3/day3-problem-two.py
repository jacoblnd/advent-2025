PUZZLE_INPUT_PATH = "../../puzzle-inputs/day3"


def get_largest_leftmost_digit_index(
    battery: str,
    rightmost_valid_index: int,
    leftmost_valid_index: int,
) -> int:
    # From the rightmost index, go backwards and find the largest leftmost digit.
    largest_digit = int(battery[rightmost_valid_index])
    largest_index = rightmost_valid_index
    for i in range(rightmost_valid_index, leftmost_valid_index-1, -1):
        # >= ensures we move as far left on the string as we can.
        if int(battery[i]) >= largest_digit:
            largest_digit = int(battery[i])
            largest_index = i
    return largest_index

def get_largest_12_digit_number(battery: str) -> int:
    # We have to start 12 back from the end of the string to guarantee
    # we can still make a 12-digit number.
    number = 0
    leftmost_valid_index = 0
    for i in range(12, 0, -1):
        magnitude = int((10 ** i) / 10)
        rightmost_valid_index = len(battery) - i
        next_index = get_largest_leftmost_digit_index(
            battery,
            rightmost_valid_index,
            leftmost_valid_index,
        )
        leftmost_valid_index = next_index+1
        number += int(battery[next_index]) * magnitude

    return number

def get_batteries():
    with open(PUZZLE_INPUT_PATH) as file:
        for line in file.readlines():
            next_line = line.strip()
            if next_line != "":
                yield next_line

def main():
    sum = 0
    for battery in get_batteries():
        sum += get_largest_12_digit_number(battery)
    print(sum)

if __name__ == "__main__":
    main()
