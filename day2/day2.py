PUZZLE_INPUT_PATH = "../../puzzle-inputs/day2"

def is_valid(id: int):
    """Check if an ID is invalid"""
    str_id = str(id)
    # We already know it can't be 2 repeated strings if 2 doesn't divide it.
    if len(str_id) == 1 or len(str_id) % 2 != 0:
        return True
    middle = int(len(str_id) / 2)
    if str_id[0:middle] == str_id[middle:]:
        return False
    return True

def get_invalid_ids(ids: list[int]) -> list[int]:
    invalid_ids = []
    for id in ids:
        if not is_valid(id):
            invalid_ids.append(id)
    return invalid_ids

def get_ids(str_range: str) -> list[int]:
    range_start, range_end = str_range.split("-")
    inclusive_range = range(int(range_start), int(range_end) + 1)
    return list(inclusive_range)

def get_str_ranges() -> list[str]:
    """Open a file and return the first line split by commas"""
    with open(PUZZLE_INPUT_PATH) as file:
        line = file.readline()
    return line.split(',')

def main():
    str_ranges = get_str_ranges()
    # print(f"Ranges: {str_ranges}",)
    invalid_ids = []
    for str_range in str_ranges:
        new_invalid_ids = get_invalid_ids(get_ids(str_range))
        invalid_ids.extend(new_invalid_ids)
    print(sum(invalid_ids))


if __name__ == "__main__":
    main()

