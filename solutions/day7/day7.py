"""Day 7: Laboratories - Advent of Code 2025."""

from solutions.utils import get_input


def simulate_beams(data: str) -> int:
    """Simulate tachyon beams and count the number of splits.

    Beams start at S and move downward. When hitting a splitter (^),
    the beam stops and two new beams are emitted left and right.

    Args:
        data: The puzzle input (manifold diagram)

    Returns:
        Number of times a beam is split
    """
    lines = data.strip().split("\n")
    rows = len(lines)
    cols = len(lines[0]) if rows > 0 else 0

    # Find starting position (S)
    start_col = -1
    for col, char in enumerate(lines[0]):
        if char == "S":
            start_col = col
            break

    if start_col == -1:
        return 0

    # Track active beams as a set of column positions
    # Beams move downward one row at a time
    active_beams: set[int] = {start_col}
    split_count = 0

    # Process row by row, starting from row 1 (below S)
    for row in range(1, rows):
        if not active_beams:
            break

        new_beams: set[int] = set()

        for col in active_beams:
            if col < 0 or col >= cols:
                # Beam exited the manifold
                continue

            char = lines[row][col]
            if char == "^":
                # Beam hits a splitter - emit two new beams left and right
                split_count += 1
                if col - 1 >= 0:
                    new_beams.add(col - 1)
                if col + 1 < cols:
                    new_beams.add(col + 1)
            else:
                # Beam continues downward
                new_beams.add(col)

        active_beams = new_beams

    return split_count


def part1(data: str) -> int:
    """Solve part 1 of the puzzle.

    Count how many times the beam is split.

    Args:
        data: The puzzle input

    Returns:
        Number of beam splits
    """
    return simulate_beams(data)


def count_timelines(data: str) -> int:
    """Count the number of distinct timelines through the manifold.

    Each split creates two timelines (left and right paths).
    Track how many timelines are at each column position.

    Args:
        data: The puzzle input (manifold diagram)

    Returns:
        Total number of distinct timelines
    """
    lines = data.strip().split("\n")
    rows = len(lines)
    cols = len(lines[0]) if rows > 0 else 0

    # Find starting position (S)
    start_col = -1
    for col, char in enumerate(lines[0]):
        if char == "S":
            start_col = col
            break

    if start_col == -1:
        return 0

    # Track number of timelines at each column position
    # Key: column, Value: number of timelines at that position
    timelines: dict[int, int] = {start_col: 1}
    finished_timelines = 0

    # Process row by row, starting from row 1 (below S)
    for row in range(1, rows):
        if not timelines:
            break

        new_timelines: dict[int, int] = {}

        for col, count in timelines.items():
            if col < 0 or col >= cols:
                # Timelines exited the manifold
                finished_timelines += count
                continue

            char = lines[row][col]
            if char == "^":
                # Each timeline splits into two
                if col - 1 >= 0:
                    new_timelines[col - 1] = new_timelines.get(col - 1, 0) + count
                if col + 1 < cols:
                    new_timelines[col + 1] = new_timelines.get(col + 1, 0) + count
            else:
                # Timelines continue downward
                new_timelines[col] = new_timelines.get(col, 0) + count

        timelines = new_timelines

    # Add remaining timelines that reached the bottom
    finished_timelines += sum(timelines.values())

    return finished_timelines


def part2(data: str) -> int:
    """Solve part 2 of the puzzle.

    Count the number of distinct timelines.

    Args:
        data: The puzzle input

    Returns:
        Number of timelines
    """
    return count_timelines(data)


def run() -> None:
    """Run the day 7 solutions."""
    print("Day 7: Laboratories")

    data = get_input(7)

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    run()
