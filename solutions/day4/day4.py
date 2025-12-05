"""Day 4: Printing Department - Advent of Code 2025."""

from collections.abc import Sequence

from solutions.utils import get_input


def count_adjacent_rolls(grid: Sequence[Sequence[str]], row: int, col: int) -> int:
    """Count the number of paper rolls adjacent to a position.

    Checks all 8 directions (including diagonals).

    Args:
        grid: The grid of paper rolls
        row: Row position to check around
        col: Column position to check around

    Returns:
        Number of adjacent paper rolls (@)
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    count = 0

    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself

            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
                count += 1

    return count


def find_accessible_rolls(grid: Sequence[Sequence[str]]) -> list[tuple[int, int]]:
    """Find rolls of paper that can be accessed by a forklift.

    A roll is accessible if it has fewer than 4 adjacent rolls.

    Args:
        grid: The grid of paper rolls

    Returns:
        List of (row, col) positions of accessible rolls
    """
    accessible = []

    for row, line in enumerate(grid):
        for col, cell in enumerate(line):
            if cell == "@":
                adjacent = count_adjacent_rolls(grid, row, col)
                if adjacent < 4:
                    accessible.append((row, col))

    return accessible


def part1(data: str) -> int:
    """Solve part 1 of the puzzle.

    Count how many rolls of paper can be accessed by a forklift.

    Args:
        data: The puzzle input (grid of paper rolls)

    Returns:
        Number of accessible rolls
    """
    grid = data.strip().split("\n")
    return len(find_accessible_rolls(grid))


def remove_rolls(grid: list[list[str]], positions: list[tuple[int, int]]) -> None:
    """Remove rolls at the given positions.

    Args:
        grid: The grid of paper rolls (modified in place)
        positions: List of (row, col) positions to remove
    """
    for row, col in positions:
        grid[row][col] = "."


def part2(data: str) -> int:
    """Solve part 2 of the puzzle.

    Repeatedly remove accessible rolls until no more can be removed.

    Args:
        data: The puzzle input (grid of paper rolls)

    Returns:
        Total number of rolls removed
    """
    # Convert to list of lists for mutability
    grid = [list(line) for line in data.strip().split("\n")]
    total_removed = 0

    while True:
        accessible = find_accessible_rolls(grid)
        if not accessible:
            break
        remove_rolls(grid, accessible)
        total_removed += len(accessible)

    return total_removed


def run() -> None:
    """Run the day 4 solutions."""
    print("Day 4: Printing Department")

    data = get_input(4)

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    run()
