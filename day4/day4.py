PUZZLE_INPUT_PATH = "../../puzzle-inputs/day4"

ROLL_CHAR = "@"
MAX_ADJACENT_ROLLS = 3

def is_corner(i: int, j: int, grid: list[str]):
    if i == 0 and j == 0:
        return True
    if i == 0 and j == len(grid[0])-1:
        return True
    if i == len(grid) - 1 and j == 0:
        return True
    if i == len(grid) - 1 and j == len(grid[0])-1:
        return True
    return False

def out_of_bounds(i: int, j: int, grid: list[str]) -> bool:
    return i < 0 or j < 0 or i >= len(grid) or j >= len(grid[0])


def is_accessible(i: int, j: int, grid: list[str]) -> bool:
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
    accessible_rolls = 0
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == ROLL_CHAR and is_accessible(i, j, grid):
                    accessible_rolls += 1

    return accessible_rolls

def build_grid():
    with open(PUZZLE_INPUT_PATH) as file:
        return [line.strip() for line in file.readlines()]


if __name__ == "__main__":
    print(check_grid(build_grid()))
