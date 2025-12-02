"""Day 2: Gift Shop - Advent of Code 2025."""

from solutions.utils import get_input


def is_repeated_sequence(n: int, min_repeats: int = 2) -> bool:
    """Check if a number is made of a sequence of digits repeated.

    Args:
        n: The number to check
        min_repeats: Minimum number of times the sequence must repeat

    Returns:
        True if the number is a repeated sequence (e.g., 55, 6464, 123123)
    """
    s = str(n)
    length = len(s)

    # Try all possible base sequence lengths
    for base_len in range(1, length // min_repeats + 1):
        if length % base_len != 0:
            continue

        repeats = length // base_len
        if repeats < min_repeats:
            continue

        base = s[:base_len]
        if base * repeats == s:
            return True

    return False


def parse_ranges(data: str) -> list[tuple[int, int]]:
    """Parse product ID ranges from input.

    Args:
        data: The puzzle input (comma-separated ranges)

    Returns:
        List of (start, end) tuples
    """
    ranges = []
    # Handle potential whitespace/newlines in input
    clean_data = data.replace("\n", "").replace(" ", "")

    for part in clean_data.split(","):
        if not part:
            continue
        start, end = part.split("-")
        ranges.append((int(start), int(end)))

    return ranges


def find_invalid_ids_in_range(start: int, end: int, min_repeats: int = 2) -> list[int]:
    """Find all invalid IDs (repeated sequences) in a range.

    Args:
        start: Start of range (inclusive)
        end: End of range (inclusive)
        min_repeats: Minimum number of times the sequence must repeat

    Returns:
        List of invalid IDs in the range
    """
    invalid_ids = []
    for n in range(start, end + 1):
        if is_repeated_sequence(n, min_repeats):
            invalid_ids.append(n)
    return invalid_ids


def part1(data: str) -> int:
    """Solve part 1 of the puzzle.

    Find all invalid IDs (sequences repeated exactly twice) in the given ranges
    and return their sum.

    Args:
        data: The puzzle input

    Returns:
        Sum of all invalid IDs
    """
    ranges = parse_ranges(data)
    total = 0

    for start, end in ranges:
        # For part 1, we need exactly 2 repeats (even-length numbers only)
        for n in range(start, end + 1):
            s = str(n)
            if len(s) % 2 == 0:
                half = len(s) // 2
                if s[:half] == s[half:]:
                    total += n

    return total


def part2(data: str) -> int:
    """Solve part 2 of the puzzle.

    Find all invalid IDs (sequences repeated at least twice) in the given ranges
    and return their sum.

    Args:
        data: The puzzle input

    Returns:
        Sum of all invalid IDs
    """
    ranges = parse_ranges(data)
    total = 0

    for start, end in ranges:
        invalid_ids = find_invalid_ids_in_range(start, end, min_repeats=2)
        total += sum(invalid_ids)

    return total


def run() -> None:
    """Run the day 2 solutions."""
    print("Day 2: Gift Shop")

    data = get_input(2)

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    run()
