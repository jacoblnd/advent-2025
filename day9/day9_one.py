from itertools import combinations

# This is just brute-forcing max area.
# Iterate through all combinations of 497 pick 2.

PUZZLE_INPUT_PATH = "../../puzzle-inputs/day9"

def calc_area(point1: tuple[int, int], point2: tuple[int, int]):
    # We need to add 1 to each below as we count the row or column which the
    # corner is in as well as the difference.
    return (abs(point1[0] - point2[0]) + 1) * (abs(point1[1] - point2[1]) + 1)

def read_points():
    with open(PUZZLE_INPUT_PATH) as file:
        lines = file.readlines()
    points = [line.strip().split(",") for line in lines]
    # Remove anything funky like a final newline.
    cleaned_points = [point for point in points if len(point) == 2]
    int_points = []
    for point in cleaned_points:
        int_points.append(
            (int(point[0]), int(point[1]))
        )
    return int_points

def main():
    points = read_points()
    max_area = 0
    for (point1, point2) in combinations(points, 2):
        area = calc_area(point1, point2)
        if area > max_area:
            max_area = area
    print(max_area)


if __name__ == "__main__":
    main()
