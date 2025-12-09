"""Brute-forcing this with recursion does not work.

Here's an alternative method to evaluate each row iteratively by summing "timeline magnitudes".

Treat the index of each row as having a beam or not. Each beam has
a "timeline magnitude". The initial timeline magnitude of the first beam is 1.
Moving through empty space results in the beam moving its timeline magnitude directly down.
Splitting results in copying the timeline magnitude down left and down right.
For the case in which multiple beams occupy the same space, their timeline magnitudes are summed
to form a new beam.

----------S---------- Source beam with timeline magnitude 1.
----------|---------- Beam moves down and retains magnitude 1.
---------|^|--------- Beam is copied: 2 beams with timeline magnitude 1.
--------|^|^|-------- Outside beams move down and have magnitude 1. Inner sums and becomes mag 2.
-------|^|^|^|------- Final result is sum of magnitudes of beams. Here it is: 8
"""
PUZZLE_INPUT_PATH = "../../puzzle-inputs/day7"

SOURCE_CHAR = 'S'
SPLITTER_CHAR = '^'


def update_beams(grouping_beams, beam_index, beam_magnitude):
    if beam_index in grouping_beams:
        grouping_beams[beam_index] += beam_magnitude
    else:
        grouping_beams[beam_index] = beam_magnitude

    return grouping_beams

def count_timelines(lines, source_index):
    # Keep track of collisions of beams and their magnitudes with a dict.
    current_beams = {source_index: 1}
    for line in lines:
        next_line_beams = {}
        for beam_index, beam_magnitude in current_beams.items():
            # Check space below the beam.
            if line[beam_index] == SPLITTER_CHAR:
                # Copy the beam's timeline magnitude to left and right.
                next_line_beams = update_beams(next_line_beams, beam_index+1, beam_magnitude)
                next_line_beams = update_beams(next_line_beams, beam_index-1, beam_magnitude)
            else:
                # The beam stays where it is with its current magnitude.
                next_line_beams = update_beams(next_line_beams, beam_index, beam_magnitude)

        current_beams = next_line_beams
    return sum([val for val in current_beams.values()])

def get_source_index(line) -> int:
    for index, char in enumerate(line):
        if char == SOURCE_CHAR:
            return index

def main():
    with open(PUZZLE_INPUT_PATH) as file:
        lines = file.readlines()
    source_index = get_source_index(lines[0])
    print(count_timelines(lines[1:], source_index))

if __name__ == "__main__":
    main()
