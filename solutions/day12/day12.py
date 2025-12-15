"""Day 12: Christmas Tree Farm - Advent of Code 2025."""

from solutions.utils import get_input


def parse_shape(lines: list[str]) -> set[tuple[int, int]]:
    """Parse a shape from lines into a set of (row, col) coordinates."""
    coords = set()
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == "#":
                coords.add((r, c))
    return coords


def normalize_shape(coords: set[tuple[int, int]]) -> frozenset[tuple[int, int]]:
    """Normalize shape to start at (0, 0)."""
    if not coords:
        return frozenset()
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    return frozenset((r - min_r, c - min_c) for r, c in coords)


def rotate_90(coords: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """Rotate shape 90 degrees clockwise."""
    return {(c, -r) for r, c in coords}


def flip_horizontal(coords: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """Flip shape horizontally."""
    return {(r, -c) for r, c in coords}


def get_all_orientations(coords: set[tuple[int, int]]) -> list[frozenset[tuple[int, int]]]:
    """Get all unique orientations (rotations and flips) of a shape."""
    orientations = set()
    current = coords

    for _ in range(4):
        orientations.add(normalize_shape(current))
        orientations.add(normalize_shape(flip_horizontal(current)))
        current = rotate_90(current)

    return list(orientations)


def parse_input(
    data: str,
) -> tuple[dict[int, list[frozenset[tuple[int, int]]]], list[tuple[int, int, list[int]]]]:
    """Parse the puzzle input.

    Returns:
        Tuple of (shapes dict mapping index to orientations, list of regions)
    """
    sections = data.strip().split("\n\n")

    # Find where regions start (lines with 'x' in them like "4x4:")
    shape_lines = []
    region_lines = []

    in_regions = False
    for section in sections:
        lines = section.strip().split("\n")
        if "x" in lines[0] and ":" in lines[0]:
            in_regions = True
        if in_regions:
            region_lines.extend(lines)
        else:
            shape_lines.append(section)

    # Parse shapes
    shapes = {}
    for section in shape_lines:
        lines = section.strip().split("\n")
        header = lines[0]
        idx = int(header.split(":")[0])
        shape_data = lines[1:]
        coords = parse_shape(shape_data)
        shapes[idx] = get_all_orientations(coords)

    # Parse regions
    regions = []
    for line in region_lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(":")
        dims = parts[0].strip()
        width, height = map(int, dims.split("x"))
        counts = list(map(int, parts[1].strip().split()))
        regions.append((width, height, counts))

    return shapes, regions


def precompute_placements(
    orientations: list[frozenset[tuple[int, int]]], width: int, height: int
) -> list[frozenset[tuple[int, int]]]:
    """Precompute all valid placements for a shape's orientations on the grid."""
    placements = []
    seen = set()

    for orientation in orientations:
        max_r = max(r for r, c in orientation)
        max_c = max(c for r, c in orientation)

        for anchor_r in range(height - max_r):
            for anchor_c in range(width - max_c):
                cells = frozenset((anchor_r + dr, anchor_c + dc) for dr, dc in orientation)
                if cells not in seen:
                    seen.add(cells)
                    placements.append(cells)

    return placements


def solve_region(
    shapes: dict[int, list[frozenset[tuple[int, int]]]], width: int, height: int, counts: list[int]
) -> bool:
    """Try to fit all required presents into the region using backtracking."""
    # Build list of all shapes to place with their valid placements
    to_place: list[list[frozenset[tuple[int, int]]]] = []
    total_cells_needed = 0

    for shape_idx, count in enumerate(counts):
        if shape_idx in shapes and count > 0:
            shape_size = len(next(iter(shapes[shape_idx])))
            total_cells_needed += shape_size * count
            placements = precompute_placements(shapes[shape_idx], width, height)
            if not placements:
                return False  # Shape can't fit at all
            for _ in range(count):
                to_place.append(placements)

    if not to_place:
        return True

    # Early pruning: check if total cells needed exceeds grid size
    if total_cells_needed > width * height:
        return False

    # Sort by number of placements (fewer first) - more constrained shapes first
    to_place.sort(key=lambda x: len(x))

    # Use a set for O(1) lookup of occupied cells
    occupied: set[tuple[int, int]] = set()

    def backtrack(idx: int) -> bool:
        if idx == len(to_place):
            return True

        placements = to_place[idx]

        for placement in placements:
            # Check if placement conflicts with occupied cells
            if not (placement & occupied):
                occupied.update(placement)
                if backtrack(idx + 1):
                    return True
                occupied.difference_update(placement)

        return False

    return backtrack(0)


def part1(data: str) -> int:
    """Solve part 1 of the puzzle.

    Count how many regions can fit all their listed presents.

    Args:
        data: The puzzle input

    Returns:
        Number of regions that can fit all presents
    """
    shapes, regions = parse_input(data)

    count = 0
    for width, height, shape_counts in regions:
        if solve_region(shapes, width, height, shape_counts):
            count += 1

    return count


def run() -> None:
    """Run the day 12 solutions."""
    print("Day 12: Christmas Tree Farm")

    data = get_input(12)

    result1 = part1(data)
    print(f"Part 1: {result1}")


if __name__ == "__main__":
    run()
