"""Day 3: Lobby - Advent of Code 2025."""

from solutions.utils import get_input


def max_joltage(bank: str, num_batteries: int = 2) -> int:
    """Find the maximum joltage from a battery bank.

    We need to pick exactly num_batteries batteries (digits) to form a number.
    The goal is to maximize this number.

    Strategy (greedy): For each position in the result, pick the largest
    available digit that still leaves enough digits remaining for the rest.

    Args:
        bank: A string of digits representing battery joltages
        num_batteries: Number of batteries to select (default 2)

    Returns:
        The maximum joltage possible
    """
    n = len(bank)
    result = []
    start = 0  # Current starting position to search from

    for i in range(num_batteries):
        # We need (num_batteries - i - 1) more digits after this one
        remaining_needed = num_batteries - i - 1
        # Latest position we can pick from to still have enough digits
        end = n - remaining_needed

        # Find the maximum digit in the valid range
        best_pos = start
        for pos in range(start, end):
            if bank[pos] > bank[best_pos]:
                best_pos = pos

        result.append(bank[best_pos])
        start = best_pos + 1  # Next digit must come after this one

    return int("".join(result))


def part1(data: str) -> int:
    """Solve part 1 of the puzzle.

    Find the maximum joltage from each bank and sum them.

    Args:
        data: The puzzle input (one bank per line)

    Returns:
        Total output joltage
    """
    total = 0
    for line in data.strip().split("\n"):
        if line:
            total += max_joltage(line)
    return total


def part2(data: str) -> int:
    """Solve part 2 of the puzzle.

    Find the maximum joltage from each bank using 12 batteries and sum them.

    Args:
        data: The puzzle input (one bank per line)

    Returns:
        Total output joltage
    """
    total = 0
    for line in data.strip().split("\n"):
        if line:
            total += max_joltage(line, num_batteries=12)
    return total


def run() -> None:
    """Run the day 3 solutions."""
    print("Day 3: Lobby")

    data = get_input(3)

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    run()
