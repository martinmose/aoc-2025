"""Day 1: Secret Entrance - Advent of Code 2025."""

from solutions.utils import get_input


def parse_rotations(data: str) -> list[tuple[str, int]]:
    """Parse rotation instructions from input.

    Args:
        data: The puzzle input

    Returns:
        List of (direction, distance) tuples
    """
    rotations = []
    for line in data.strip().splitlines():
        direction = line[0]
        distance = int(line[1:])
        rotations.append((direction, distance))
    return rotations


def part1(data: str) -> int:
    """Solve part 1 of the puzzle.

    Count how many times the dial points at 0 after a rotation.
    Dial starts at 50, wraps around 0-99.

    Args:
        data: The puzzle input

    Returns:
        Number of times dial points at 0
    """
    rotations = parse_rotations(data)
    position = 50
    zero_count = 0

    for direction, distance in rotations:
        if direction == "L":
            position = (position - distance) % 100
        else:  # R
            position = (position + distance) % 100

        if position == 0:
            zero_count += 1

    return zero_count


def part2(data: str) -> int:
    """Solve part 2 of the puzzle.

    Count every time the dial points at 0 during any click,
    not just at the end of rotations.

    Args:
        data: The puzzle input

    Returns:
        Total times dial points at 0 (during and after rotations)
    """
    rotations = parse_rotations(data)
    position = 50
    zero_count = 0

    for direction, distance in rotations:
        if direction == "L":
            new_position = (position - distance) % 100
        else:  # R
            new_position = (position + distance) % 100

        # Count full rotations (each full rotation crosses 0 once)
        full_rotations = distance // 100
        zero_count += full_rotations

        # Check if we cross 0 in the partial rotation
        remainder = distance % 100
        if remainder > 0:
            if direction == "L":
                # Moving left from position by remainder clicks
                # We cross 0 if position < remainder (we wrap around)
                # But NOT if position == 0 (we're leaving 0, not crossing it)
                if position != 0 and position < remainder:
                    zero_count += 1
                elif position == 0 and remainder == 100:
                    # Edge case: full wrap from 0
                    zero_count += 1
                elif new_position == 0 and position != 0:
                    # Landing exactly on 0
                    zero_count += 1
            else:  # R
                # Moving right from position by remainder clicks
                # We cross 0 if position + remainder >= 100 (we wrap around)
                # But NOT if position == 0 (we're leaving 0, not crossing it)
                if position != 0 and position + remainder >= 100:
                    zero_count += 1
                elif new_position == 0 and position != 0:
                    # Landing exactly on 0
                    zero_count += 1

        position = new_position

    return zero_count


def run() -> None:
    """Run the day 1 solutions."""
    print("Day 1: Secret Entrance")

    data = get_input(1)

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    run()
