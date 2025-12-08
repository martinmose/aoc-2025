"""Day 6: Trash Compactor - Advent of Code 2025."""

import math

from solutions.utils import get_input


def parse_problems(data: str) -> list[tuple[list[int], str]]:
    """Parse the worksheet into individual problems.

    Each problem is a tuple of (numbers, operation).

    Args:
        data: The puzzle input (columnar worksheet)

    Returns:
        List of (numbers, operation) tuples
    """
    lines = data.split("\n")
    if not lines:
        return []

    # Pad all lines to the same length
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]

    # Find column boundaries by looking for all-space columns
    # Problems are separated by columns that are entirely spaces
    num_rows = len(lines)
    problems = []

    # Track which columns belong to which problem
    col = 0
    while col < max_len:
        # Skip separator columns (all spaces)
        while col < max_len and all(lines[row][col] == " " for row in range(num_rows)):
            col += 1

        if col >= max_len:
            break

        # Find the end of this problem (next all-space column or end)
        start_col = col
        while col < max_len and not all(lines[row][col] == " " for row in range(num_rows)):
            col += 1

        # Extract the problem from start_col to col
        problem_lines = [line[start_col:col] for line in lines]

        # Last line contains the operation
        op_line = problem_lines[-1].strip()
        operation = op_line if op_line in ("+", "*") else None

        if operation:
            # Parse numbers from the lines above the operation
            numbers = []
            for line in problem_lines[:-1]:
                stripped = line.strip()
                if stripped:
                    numbers.append(int(stripped))
            problems.append((numbers, operation))

    return problems


def solve_problem(numbers: list[int], operation: str) -> int:
    """Solve a single math problem.

    Args:
        numbers: List of numbers to combine
        operation: Either "+" for sum or "*" for product

    Returns:
        The result of the operation
    """
    if operation == "+":
        return sum(numbers)
    else:  # "*"
        return math.prod(numbers)


def part1(data: str) -> int:
    """Solve part 1 of the puzzle.

    Solve all problems and return the grand total.

    Args:
        data: The puzzle input

    Returns:
        Sum of all problem answers
    """
    problems = parse_problems(data)
    return sum(solve_problem(numbers, op) for numbers, op in problems)


def parse_problems_vertical(data: str) -> list[tuple[list[int], str]]:
    """Parse the worksheet into individual problems using vertical reading.

    Numbers are read column by column (top digit to bottom digit).
    Each problem is a tuple of (numbers, operation).

    Args:
        data: The puzzle input (columnar worksheet)

    Returns:
        List of (numbers, operation) tuples
    """
    lines = data.split("\n")
    if not lines:
        return []

    # Pad all lines to the same length
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]

    num_rows = len(lines)
    problems = []

    # Track which columns belong to which problem
    col = 0
    while col < max_len:
        # Skip separator columns (all spaces)
        while col < max_len and all(lines[row][col] == " " for row in range(num_rows)):
            col += 1

        if col >= max_len:
            break

        # Find the end of this problem (next all-space column or end)
        start_col = col
        while col < max_len and not all(lines[row][col] == " " for row in range(num_rows)):
            col += 1

        # Extract the problem columns from start_col to col
        # Last row contains the operation
        op_line = lines[-1][start_col:col].strip()
        operation = op_line if op_line in ("+", "*") else None

        if operation:
            # Read numbers vertically - each column is a number
            # Top-to-bottom gives most significant to least significant digit
            numbers = []
            for c in range(start_col, col):
                digits = ""
                for row in range(num_rows - 1):  # Exclude operation row
                    char = lines[row][c]
                    if char.isdigit():
                        digits += char
                if digits:
                    numbers.append(int(digits))
            problems.append((numbers, operation))

    return problems


def part2(data: str) -> int:
    """Solve part 2 of the puzzle.

    Solve all problems using vertical number reading and return the grand total.

    Args:
        data: The puzzle input

    Returns:
        Sum of all problem answers
    """
    problems = parse_problems_vertical(data)
    return sum(solve_problem(numbers, op) for numbers, op in problems)


def run() -> None:
    """Run the day 6 solutions."""
    print("Day 6: Trash Compactor")

    data = get_input(6)

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    run()
