# Early notes to start the problem: (they do not capture the full logic of the program)
# Use last line to determine associations with operators.
# Build map of column index to operator.
# Go through each line adding new int to column or
# For each column:
#   Keep track of the mode we're in:
#       Adding digits to number _or_
#       Waiting for new number to begin
#   Keep track of current number
#   Keep track of the full list of numbers so far for that column.
#   If we're adding digits to number:
#       and we see a digit: add it
#       and we see a space: calculate the number and add it to the list. Switch modes.
#   If we're waiting for a new number to begin:
#       and we see a digit: create a new current number string with number. Switch modes.
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

class Column:
    """Columns capture the list of numbers in a column in past_nums.

    Columns expect to be given digit characters one-at-a-time moving down the column. They would be
    more useful for a more complicated problem if there were multiple numbers per column but it
    seems that there's generally only one. I should have looked deeper into the file earlier to
    realize that I could write a simpler structure due to that constraint.
    """
    past_nums: list[int]
    num_accumulator: str

    def __init__(self, nums, num_accumulator):
        self.past_nums = nums
        self.num_accumulator = num_accumulator

    @staticmethod
    def from_first_char(first_char: str) -> Column:
        return Column(nums=[], num_accumulator=first_char)

    def calculate_current(self) -> int:
        return int(self.num_accumulator)

    def parse_space(self):
        # A space has been observed in the column.
        if self.num_accumulator:
            self.past_nums.append(self.calculate_current())
            # Reset self.current_num to something falsy which we use to imply what "mode" we're in
            self.num_accumulator = ''

    def parse_char(self, char: str):
        # A char has been observed in the column.
        if self.num_accumulator:
            self.num_accumulator = self.num_accumulator + char
        else:
            self.num_accumulator = char

    def complete_parse(self):
        # complete_parse is equivalent to calling parse_space but exists to logically separate
        # concerns of parsing any given space and finishing parsing completely.
        # parse_space must be called again at the end as our num_accumulator may still be counting
        # num characters.
        if self.num_accumulator:
            self.parse_space()


class ColumnGroup:
    columns: list[Column]
    operator: str

    def __init__(self, columns, operator):
        self.columns = columns
        self.operator = operator

    def calculate_total(self):
        # Perform operation on all values in all columns.
        all_nums = []
        for col in self.columns:
            all_nums.extend(col.past_nums)
        return reduce(R_FUNC[self.operator], all_nums, R_ACC[self.operator])

def main():
    with open(PUZZLE_INPUT_PATH) as file:
        lines = file.readlines()
    COL_INDEX_MAP = {}
    last_line = lines[-1]
    # Populate Columns from all but last line which contains operators.
    for line in lines[:len(lines)-1]:
        for char_index, char in enumerate(line):
            if char == ' ':
                if char_index in COL_INDEX_MAP:
                    COL_INDEX_MAP[char_index].parse_space()
            # Char must be a digit or a newline.
            elif char != '\n':
                if char_index in COL_INDEX_MAP:
                    COL_INDEX_MAP[char_index].parse_char(char)
                else:
                    COL_INDEX_MAP[char_index] = Column.from_first_char(char)
    # Ensure we finish parsing any in-flight numbers being accumulated.
    [c.complete_parse() for c in COL_INDEX_MAP.values()]
    # Invalid indices are columns which are the single-space delimiters.
    # Valid indices contain number data.
    valid_indices = sorted(COL_INDEX_MAP.keys())
    # Column groups are formed from contiguous valid indices.
    # Determine groups and the group total as we go
    # We know 0 is a valid index.
    last_valid_index = 0
    group_indices = [0]
    group_operator = last_line[0]
    COL_GROUPS = []
    for valid_index in valid_indices[1:]:
        # Check if we skipped over to the next group.
        if valid_index - last_valid_index != 1:
            # We are in a new group. We know the bounds of the old group.
            # Calculate it.
            COL_GROUPS.append(
                ColumnGroup(
                    columns=[COL_INDEX_MAP[i] for i in group_indices],
                    operator=group_operator
                )
            )
            # Reset.
            group_operator = last_line[valid_index]
            group_indices = [valid_index]
            last_valid_index = valid_index
        else:
            group_indices.append(valid_index)
            last_valid_index = valid_index
    # Grab last straggler group.
    COL_GROUPS.append(
        ColumnGroup(
            columns=[COL_INDEX_MAP[i] for i in group_indices],
            operator=group_operator
        )
    )
    print(sum([g.calculate_total() for g in COL_GROUPS]))

if __name__ == "__main__":
    main()
