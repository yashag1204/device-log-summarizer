"""Sensor-reading cleaning logic for Section 1."""

from typing import Any


def clean_sensor_readings(values: list[Any]) -> list[float]:
    """Convert values to floats; drop invalid, null, and negative values.

    Values greater than 500.0 are clipped to 500.0. Empty or fully invalid
    input returns an empty list.
    """
    cleaned: list[float] = []

    for value in values:
        if value is None:
            continue

        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError):
            continue

        # NaN and infinities are not meaningful sensor readings.
        if number != number or number in (float("inf"), float("-inf")):
            continue
        if number < 0:
            continue

        cleaned.append(min(number, 500.0))

    return cleaned


if __name__ == "__main__":
    cases = [
        (["12.5", 20, None, -1, "bad", 800], [12.5, 20.0, 500.0]),
        ([], []),
        ([None, "oops", -9], []),
    ]

    for index, (values, expected) in enumerate(cases, start=1):
        actual = clean_sensor_readings(values)
        assert actual == expected, f"Case {index}: expected {expected}, got {actual}"
        print(f"Test {index} passed: {actual}")
