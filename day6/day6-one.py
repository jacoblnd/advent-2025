from functools import reduce

PUZZLE_INPUT_PATH = "../../puzzle-inputs/day6"

# Try to get a little fancy with a DRY reduce for fun.
# Reduce Func
R_FUNC = {
    "+": lambda x,y: x+y,
    "*": lambda x,y: x*y
}
# Reduce accumulator.
R_ACC = {
    "+": 0,
    "*": 1,
}

def read_cephalopod_homework() -> tuple[list[list[int]], list[str]]:
    """Read cephalopod homework data as rows of ints.

    Return the last line containing operators as the second element of the return tuple.
    """
    int_rows = []
    operator_row = None
    with open(PUZZLE_INPUT_PATH) as file:
        lines = file.readlines()
        last_line = lines[-1]
        for line in lines:
            # Check if we're on the last line which is operators
            if line is last_line:
                operator_row = line.strip().split()
            else:
                int_rows.append([int(str_num) for str_num in line.strip().split()])
    return int_rows, operator_row

def evaluate(nums: list[int], operator: str):
    if operator == '+':
        return sum(nums)
    elif operator == "*":
        return

def main():
    int_rows, operator_row = read_cephalopod_homework()
    # Pivot rows to cols.
    col_data: list[list[int]] = []
    for row_index, row in enumerate(int_rows):
        for col_index, col in enumerate(row):
            # The column doesn't exist yet. Create it.
            if row_index == 0:
                col_data.append([col])
            else:
                col_data[col_index].append(col)
    col_results = [
        reduce(R_FUNC[op], nums, R_ACC[op])
        for nums, op in zip(col_data, operator_row)
    ]
    print(sum(col_results))


if __name__ == "__main__":
    main()
