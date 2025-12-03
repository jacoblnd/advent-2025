use super::*;

#[test]
fn safe_right_one() {
    let mut safe = Safe { dial_value: 50 };
    let passes = safe.rotate(Rotation {
        clicks: 1,
        direction: RotationDirection::Right,
    });
    assert_eq!(safe.dial_value, 51);
    assert_eq!(passes, 0);
}
#[test]
fn safe_left_one() {
    let mut safe = Safe { dial_value: 50 };
    let passes = safe.rotate(Rotation {
        clicks: 1,
        direction: RotationDirection::Left,
    });
    assert_eq!(safe.dial_value, 49);
    assert_eq!(passes, 0);
}
#[test]
fn safe_right_rollover_to_zero() {
    let mut safe = Safe { dial_value: 50 };
    let passes = safe.rotate(Rotation {
        clicks: 50,
        direction: RotationDirection::Right,
    });
    assert_eq!(safe.dial_value, 0);
    assert_eq!(passes, 0);
}
#[test]
fn safe_left_rollover() {
    let mut safe = Safe { dial_value: 1 };
    let passes = safe.rotate(Rotation {
        clicks: 102,
        direction: RotationDirection::Left,
    });
    assert_eq!(safe.dial_value, 99);
    assert_eq!(passes, 2);
}
#[test]
fn safe_left_rollover_to_zero() {
    let mut safe = Safe { dial_value: 50 };
    let passes = safe.rotate(Rotation {
        clicks: 150,
        direction: RotationDirection::Left,
    });
    assert_eq!(safe.dial_value, 0);
    assert_eq!(passes, 1);
}
#[test]
fn safe_right_large_rollover() {
    let mut safe = Safe { dial_value: 50 };
    let passes = safe.rotate(Rotation {
        clicks: 200,
        direction: RotationDirection::Right,
    });
    assert_eq!(safe.dial_value, 50);
    assert_eq!(passes, 2);
}
#[test]
fn safe_left_large_rollover() {
    let mut safe = Safe { dial_value: 50 };
    let passes = safe.rotate(Rotation {
        clicks: 200,
        direction: RotationDirection::Left,
    });
    assert_eq!(safe.dial_value, 50);
    assert_eq!(passes, 2);
}
#[test]
fn safe_right_large_rollover_to_zero() {
    let mut safe = Safe { dial_value: 1 };
    let passes = safe.rotate(Rotation {
        clicks: 199,
        direction: RotationDirection::Right,
    });
    assert_eq!(safe.dial_value, 0);
    assert_eq!(passes, 1);
}
#[test]
fn safe_zero_left_rollover() {
    let mut safe = Safe { dial_value: 0 };
    let passes = safe.rotate(Rotation {
        clicks: 1,
        direction: RotationDirection::Left,
    });
    assert_eq!(safe.dial_value, 99);
    assert_eq!(passes, 0);
}
