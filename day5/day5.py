PUZZLE_INPUT_PATH = "../../puzzle-inputs/day5"

def read_id(line: str) -> int:
    return int(line.strip())

def read_range(line: str) -> tuple[int, int]:
    start, end = line.strip().split("-")
    return int(start), int(end)

def load_ranges_and_ids() -> tuple[list[tuple[int, int]], list[int]]:
    id_ranges: list[tuple[int, int]] = []
    ids_to_check: list[int] = []
    reading_ranges = True
    with open(PUZZLE_INPUT_PATH) as file:
        for line in file.readlines():
            # Handle case where we need to switch:
            if line.strip() == "":
                reading_ranges = False
                continue
            if reading_ranges:
                id_ranges.append(read_range(line))
            else:
                ids_to_check.append(read_id(line))
    return id_ranges, ids_to_check

def in_range(id_to_check: int, id_range: tuple[int, int]):
    return id_to_check >= id_range[0] and id_to_check <= id_range[1]

def count_distinct_range(id_range: tuple[int, int]) -> int:
    return id_range[1] - id_range[0] + 1

def count_ranges(id_ranges: list[tuple[int, int]]) -> int:
    # Sort the input ranges by start.
    id_ranges = sorted(id_ranges, key=lambda r: r[0])
    current_range_start = id_ranges[0][0]
    current_range_end = id_ranges[0][1]
    fresh_ids = count_distinct_range(id_ranges[0])
    # Start with an initial current range of the first range.
    for id_range in id_ranges[1:]:
        new_range_start = id_range[0]
        new_range_end = id_range[1]
        # If new start is greater than current end then we're looking at a new distinct range.
        if new_range_start > current_range_end:
            fresh_ids += count_distinct_range(id_range)
            current_range_start = new_range_start
            current_range_end = new_range_end
        # Check if start _is_ end:
        elif new_range_start == current_range_end:
            # Don't double-count range end.
            fresh_ids += count_distinct_range(id_range) - 1
            current_range_start = current_range_end
            current_range_end = new_range_end
        # Check if start is within current range.
        elif new_range_start > current_range_start:
            # We can leave early if end is also within the range:
            if new_range_end <= current_range_end:
                current_range_start = new_range_start
            else:
                # We have start > current start and end > current end.
                # Count current_end -> new_end and update both start and end.
                # count the difference and update start and end
                fresh_ids += count_distinct_range((current_range_end+1, new_range_end))
                current_range_start = new_range_start
                current_range_end = new_range_end
        # Check if new start is equal to current start:
        elif new_range_start == current_range_start:
            # We can leave early if end is also within range:
            if new_range_end <= current_range_end:
                # don't need to update end.
                continue
            else:
                # We have start == current start and end > current_end.
                # count current_end -> new_end and update end.
                fresh_ids += count_distinct_range((current_range_end+1, new_range_end))
                current_range_end = new_range_end
    return fresh_ids

def main():
    fresh_id_ranges, ids_to_check = load_ranges_and_ids()
    count_fresh_ids = 0
    ### Problem one was pretty straightforward:
    # for id_to_check in ids_to_check:
    #     for id_range in fresh_id_ranges:
    #         if in_range(id_to_check, id_range):
    #             # ID is guaranteed fresh.
    #             count_fresh_ids += 1
    #             break
    ### Problem Two:
    print(count_ranges(fresh_id_ranges))

if __name__ == "__main__":
    main()
