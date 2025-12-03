use std::fs::read_to_string;

const PUZZLE_INPUT_FILE_PATH: &'static str = "../../puzzle-inputs/day1";
const STARTING_DIAL_VALUE: i32 = 50;
const DIAL_MAX: i32 = 99;

#[derive(Debug, Copy, Clone)]
enum RotationDirection {
    Left,
    Right,
}

#[derive(Debug)]
struct RawRotation(String);

struct Safe {
    dial_value: i32,
}

#[derive(Debug, Copy, Clone)]
struct Rotation {
    direction: RotationDirection,
    clicks: u32,
}

/// Safe was originally implemented based on the first problem of day1 and wasn't
/// refactored after seeing requirements for problem 2.
/// It's awkward now to mutate state and return a value but that's where we're at.
impl Safe {
    fn rotate(&mut self, rotation: Rotation) -> i32 {
        // We need to only count zero when we hit it the first time so we
        // track the original dial value.
        let original_dial_value = self.dial_value;
        // First determine the "absolute value" of clicks with the remainder.
        let modded_rotation = (rotation.clicks as i32) % (DIAL_MAX + 1);
        // How many full rotations did we have:
        let mut passes = (rotation.clicks as i32) / (DIAL_MAX + 1);

        // Move it left or right.
        let new_dial_value = match rotation.direction {
            RotationDirection::Left => self.dial_value - modded_rotation,
            RotationDirection::Right => self.dial_value + modded_rotation,
        };
        // Handle the cases where we went too far.
        if new_dial_value > DIAL_MAX {
            self.dial_value = new_dial_value - (DIAL_MAX + 1);
            // Ensure we don't double-count when landing on or moving from zero.
            if self.dial_value != 0 && original_dial_value != 0 {
                passes += 1;
            }
        } else if new_dial_value < 0 {
            self.dial_value = (DIAL_MAX + 1) - new_dial_value.abs();
            // Ensure we don't double-count when landing on or moving from zero.
            if self.dial_value != 0 && original_dial_value != 0 {
                passes += 1;
            }
        } else {
            self.dial_value = new_dial_value;
        }
        return passes;
    }
}

#[cfg(test)]
#[path = "unit_tests/safe.rs"]
mod tests;

/// Just for fun let's derive the From trait on a wrapped type.
/// instead of just dealing with normal Strings.
impl From<RawRotation> for Rotation {
    fn from(raw_rotation: RawRotation) -> Self {
        let mut chars_iter = raw_rotation.0.chars();
        let direction = match chars_iter.next() {
            Some(c) => match c {
                'L' => RotationDirection::Left,
                'R' => RotationDirection::Right,
                _ => panic!("First char was unexpected! {}", c),
            },
            None => panic!("raw_rotation {:?} was empty!", raw_rotation),
        };
        let rest_of_chars: String = chars_iter.collect();
        let clicks: u32 = match rest_of_chars.parse() {
            Ok(num) => num,
            Err(e) => {
                panic!("raw rotation rest of chars {rest_of_chars} could not be parsed as u32 {e}")
            }
        };
        Rotation { direction, clicks }
    }
}

fn read_lines(filename: &str) -> Vec<String> {
    let mut result = Vec::new();

    for line in read_to_string(filename).unwrap().lines() {
        if line.to_string() != "" {
            result.push(line.to_string())
        }
    }

    result
}

fn read_rotations() -> Vec<RawRotation> {
    let mut raw_rotations: Vec<RawRotation> = Vec::new();
    for line in read_lines(PUZZLE_INPUT_FILE_PATH) {
        raw_rotations.push(RawRotation(line));
    }
    raw_rotations
}

fn find_zeroes(rotations: Vec<Rotation>) -> u32 {
    let mut safe = Safe {
        dial_value: STARTING_DIAL_VALUE,
    };
    let mut num_zeroes: u32 = 0;
    for rotation in rotations {
        let additional_passes = safe.rotate(rotation);
        num_zeroes += additional_passes as u32;
        if safe.dial_value == 0 {
            num_zeroes += 1;
        }
    }
    num_zeroes
}

fn main() {
    let raw_rotations = read_rotations();
    let rotations: Vec<Rotation> = raw_rotations
        .into_iter()
        .map(|rr| Rotation::from(rr))
        .collect();
    let found_zeroes = find_zeroes(rotations);
    println!("Found {} zeroes! Neato", found_zeroes);
}
