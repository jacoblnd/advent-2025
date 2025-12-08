from copy import deepcopy

PUZZLE_INPUT_PATH = "../../puzzle-inputs/day7"

SOURCE_CHAR = 'S'
SPLITTER_CHAR = '^'

def count_splits(lines):
    """
    1. Find the source.
    2. Initialize a counter and first beam.
    3. For each line, For each beam:
        descend and determine if a split occurs and handle it.
    """
    # 1. Find the source:
    index = 0
    source_index = 0
    for index, char in enumerate(lines[0]):
        if char == SOURCE_CHAR:
            source_index = index
    # 2. Initialize counter, beams.
    # Keep track of all beams as a dict.
    beams = {}
    update_beams = {}
    count_splits = 0
    beams[source_index] = 1
    # 3. Iterate.
    for line in lines[1:]:
        for beam_index in beams.keys():
            # Copy beam.
            update_beams[beam_index] = beams[beam_index]
            # Go down one and see if it's a splitter
            if line[beam_index] == SPLITTER_CHAR:
                # Handle split: Increment counter, remove existing beam and add new beams.
                del update_beams[beam_index]
                update_beams[beam_index+1] = 1
                update_beams[beam_index-1] = 1
                count_splits += 1
        # Handle updating beams so we don't update beams.keys during iteration.
        beams = deepcopy(update_beams)
    print(count_splits)


def main():
    with open(PUZZLE_INPUT_PATH) as file:
        lines = file.readlines()
    count_splits(lines)

if __name__ == "__main__":
    main()
