"""Day 5: Cafeteria - Advent of Code 2025."""

from solutions.utils import get_input


def parse_input(data: str) -> tuple[list[tuple[int, int]], list[int]]:
    """Parse the database input into ranges and ingredient IDs.

    Args:
        data: The puzzle input

    Returns:
        Tuple of (fresh ranges, available ingredient IDs)
    """
    sections = data.strip().split("\n\n")
    
    ranges = []
    for line in sections[0].split("\n"):
        start, end = line.split("-")
        ranges.append((int(start), int(end)))
    
    ingredients = [int(line) for line in sections[1].split("\n")]
    
    return ranges, ingredients


def is_fresh(ingredient_id: int, ranges: list[tuple[int, int]]) -> bool:
    """Check if an ingredient ID is fresh.

    An ingredient is fresh if it falls within any of the fresh ranges.

    Args:
        ingredient_id: The ingredient ID to check
        ranges: List of (start, end) fresh ranges (inclusive)

    Returns:
        True if the ingredient is fresh
    """
    return any(start <= ingredient_id <= end for start, end in ranges)


def part1(data: str) -> int:
    """Solve part 1 of the puzzle.

    Count how many available ingredient IDs are fresh.

    Args:
        data: The puzzle input

    Returns:
        Number of fresh ingredients
    """
    ranges, ingredients = parse_input(data)
    return sum(1 for ingredient in ingredients if is_fresh(ingredient, ranges))


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge overlapping ranges into non-overlapping ranges.

    Args:
        ranges: List of (start, end) ranges (inclusive)

    Returns:
        List of merged non-overlapping ranges
    """
    if not ranges:
        return []

    # Sort by start, then by end
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]

    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        # Ranges overlap or are adjacent (e.g., 3-5 and 6-8 can merge to 3-8)
        if start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged


def count_fresh_ids(ranges: list[tuple[int, int]]) -> int:
    """Count the total number of unique fresh ingredient IDs.

    Args:
        ranges: List of (start, end) fresh ranges (inclusive)

    Returns:
        Total count of unique fresh IDs
    """
    merged = merge_ranges(ranges)
    return sum(end - start + 1 for start, end in merged)


def part2(data: str) -> int:
    """Solve part 2 of the puzzle.

    Count how many unique ingredient IDs are considered fresh.

    Args:
        data: The puzzle input

    Returns:
        Total number of fresh ingredient IDs
    """
    ranges, _ = parse_input(data)
    return count_fresh_ids(ranges)


def run() -> None:
    """Run the day 5 solutions."""
    print("Day 5: Cafeteria")

    data = get_input(5)

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    run()
