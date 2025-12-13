import math
from dataclasses import dataclass
from itertools import combinations

PUZZLE_INPUT_PATH = "../../puzzle-inputs/day8"

class IDGen():
    """IDGen generates monotonically increasing string ids."""
    sequence: int = 0

    @classmethod
    def get_id(cls) -> str:
        cls.sequence += 1
        return str(cls.sequence)

@dataclass
class JunctionBox():
    """JunctionBox is just a Point with an identifier.

    And the identifier happens to be a string representation of the Point.
    This problem could have been completely modeled with just the Point
    (or a tuple or namedtuple). But the domain has a JunctionBox already so we'll prematurely
    create it to localize any future JunctionBox behavior and make our code a bit more expressive
    of the domain.
    """
    id: str
    point: Point

    @staticmethod
    def from_string(input_string: str) -> JunctionBox:
        return JunctionBox(
            id=input_string.strip(),
            point=Point.from_string(input_string)
        )

@dataclass
class Point():
    x: int
    y: int
    z: int

    @staticmethod
    def from_string(input_string: str) -> Point:
        # Do super minimal cleaning. This is not a safe way to handle strings.
        cleaned_string = input_string.strip().split(',')
        return Point(
            x=int(cleaned_string[0]),
            y=int(cleaned_string[1]),
            z=int(cleaned_string[2]),
        )

def distance(point1: Point, point2: Point) -> float:
    x_diff = point1.x - point2.x
    y_diff = point1.y - point2.y
    z_diff = point1.z - point2.z
    return math.sqrt(
        (x_diff ** 2) + (y_diff ** 2) + (z_diff ** 2)
    )

def read_puzzle_file():
    with open(PUZZLE_INPUT_PATH) as file:
        return file.readlines()

def count_largest_circuits(junction_box_strings):
    junction_boxes = [
        JunctionBox.from_string(junction_box_string)
        for junction_box_string in junction_box_strings
    ]
    # Brute force look at every pair and then sort. There's probably an optimization if we
    # do some fancy weighted sorting by x, y, z?
    junction_box_pairs = []
    for l_box, r_box in combinations(junction_boxes, 2):
        junction_box_pairs.append({
            "box1": l_box,
            "box2": r_box,
            "distance": distance(l_box.point, r_box.point)
        })
    # Sort by closest distance.
    sorted_jb_pairs = sorted(junction_box_pairs, key=lambda d: d["distance"])

    # Instantiate the lookup table of circuit id to list of junction box ids within.
    # This is our source of truth for connected components.
    circuit_jb_lookup = {
        IDGen.get_id(): [junction_box.id]
        for junction_box in junction_boxes
    }
    # Instantiate the reverse lookup table of junction box id to circuit_ids:
    jb_circuit_lookup = {
        jb_ids[0]: circuit_id
        for circuit_id, jb_ids in circuit_jb_lookup.items()
    }
    # Connect the closest 1,000 junction boxes.
    for i in range(0, 1000):
        box1 = sorted_jb_pairs[i]["box1"]
        box2 = sorted_jb_pairs[i]["box2"]
        # Check if they are already connected:
        box1_circuit_id = jb_circuit_lookup[box1.id]
        box2_circuit_id = jb_circuit_lookup[box2.id]
        if box1_circuit_id == box2_circuit_id:
            continue
        # Otherwise, perform the connection:
        # 1. Mint new circuit ID
        new_circuit_id = IDGen.get_id()
        # 2. Keep track of all old circuit ids
        #   all_old_circuit_ids.
        other_jb_ids1 = circuit_jb_lookup[box1_circuit_id]
        other_jb_ids2 = circuit_jb_lookup[box2_circuit_id]
        all_old_jb_ids = list(set(other_jb_ids1 + other_jb_ids2 + [box1.id, box2.id]))
        # 3. For each old Jb id:
        #       update the jb_id:circuit_id map.
        for old_jb_id in all_old_jb_ids:
            jb_circuit_lookup[old_jb_id] = new_circuit_id
        # The only old circuits which could be part of this are box1_circuit_id and box2_circuit_id
        # 4. Delete the old circuit_ids from the circuit_id:jb_id map.
        del circuit_jb_lookup[box1_circuit_id]
        del circuit_jb_lookup[box2_circuit_id]
        # 5. Add the new circuit to the circuit_id:jb_ids map.
        circuit_jb_lookup[new_circuit_id] = all_old_jb_ids
    # Largest circuits:
    largest_values = sorted([len(circuit) for circuit in circuit_jb_lookup.values()], reverse=True)[:3]
    return largest_values

def main():
    junction_lines = read_puzzle_file()
    print(count_largest_circuits(junction_lines))

if __name__ == "__main__":
    main()
