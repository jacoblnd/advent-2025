PUZZLE_INPUT_PATH = "../../puzzle-inputs/day2"

def is_repeating(str_id: str, slice_length: int):
    """Given a string and a slice length which divides its length, return whether the value repeats"""
    total_slices = int(len(str_id) / slice_length)
    slice_start = 0
    slice_end = slice_length
    str_slices = set()
    for _ in range(0, total_slices):
        str_slices.add(str_id[slice_start:slice_end])
        slice_start += slice_length
        slice_end += slice_length
    return len(str_slices) == 1

def yield_next_divisor(total, current_divisor):
    """Iteratively find the next divisor and yield it"""
    current_value = current_divisor - 1
    while current_value != 0:
        if total % current_value == 0:
            yield current_value
        current_value -= 1

def is_valid(id: int):
    """Check if an ID is valid"""
    str_id = str(id)
    if len(str_id) == 1:
        return True
    any_repeating = [
        is_repeating(str_id, divisor)
        for divisor in yield_next_divisor(len(str_id), len(str_id))
    ]
    return not any(any_repeating)

# Part 1 solution:
# def is_valid(id: int):
#     """Check if an ID is valid"""
#     str_id = str(id)
#     # We already know it can't be 2 repeated strings if 2 doesn't divide it.
#     if len(str_id) == 1 or len(str_id) % 2 != 0:
#         return True
#     middle = int(len(str_id) / 2)
#     if str_id[0:middle] == str_id[middle:]:
#         return False
#     return True

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

