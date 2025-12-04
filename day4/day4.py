PUZZLE_INPUT_PATH = "../../puzzle-inputs/day4"

EMPTY_CHAR = "."
ROLL_CHAR = "@"
MAX_ADJACENT_ROLLS = 3

def is_corner(i: int, j: int, grid: list):
    if i == 0 and j == 0:
        return True
    if i == 0 and j == len(grid[0])-1:
        return True
    if i == len(grid) - 1 and j == 0:
        return True
    if i == len(grid) - 1 and j == len(grid[0])-1:
        return True
    return False

def out_of_bounds(i: int, j: int, grid: list) -> bool:
    return i < 0 or j < 0 or i >= len(grid) or j >= len(grid[0])


def is_accessible(i: int, j: int, grid: list) -> bool:
    # handle literal corner cases first.
    if is_corner(i, j, grid):
        return True
    checkable_values = [
        (c_i, c_j) for c_i in range(i-1, i+2) for c_j in range(j-1, j+2)
    ]
    adjacent_rolls = 0
    for c_i, c_j in checkable_values:
        if (c_i == i and c_j == j) or out_of_bounds(c_i, c_j, grid):
            continue
        if grid[c_i][c_j] == ROLL_CHAR:
            adjacent_rolls += 1
    return adjacent_rolls <= MAX_ADJACENT_ROLLS

def check_grid(grid):
    removed_rolls = 0
    new_grid = []
    for i, row in enumerate(grid):
        new_line = []
        for j, cell in enumerate(row):
            if cell == EMPTY_CHAR:
                new_line.append(EMPTY_CHAR)
            if cell == ROLL_CHAR:
                if is_accessible(i, j, grid):
                    removed_rolls += 1
                    new_line.append(EMPTY_CHAR)
                else:
                    new_line.append(ROLL_CHAR)
        new_grid.append(new_line)

    return removed_rolls, new_grid

def continuously_remove_rolls(grid):
    new_grid = grid
    removed_rolls = 0
    while True:
        newly_removed_rolls, new_grid = check_grid(new_grid)
        if newly_removed_rolls == 0:
            return removed_rolls
        else:
            removed_rolls += newly_removed_rolls

def build_grid():
    with open(PUZZLE_INPUT_PATH) as file:
        return [line.strip() for line in file.readlines()]


if __name__ == "__main__":
    # print(check_grid(build_grid()))
    print(continuously_remove_rolls(build_grid()))
