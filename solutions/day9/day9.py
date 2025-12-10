"""Day 9: Movie Theater - Advent of Code 2025."""

from itertools import combinations

from solutions.utils import get_input


def get_polygon_edges(
    red_tiles: list[tuple[int, int]],
) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """Get all edges of the polygon connecting red tiles.

    Args:
        red_tiles: List of red tile positions in order

    Returns:
        List of edges as ((x1,y1), (x2,y2)) tuples
    """
    edges = []
    n = len(red_tiles)
    for i in range(n):
        p1 = red_tiles[i]
        p2 = red_tiles[(i + 1) % n]
        edges.append((p1, p2))
    return edges


def point_in_polygon(point: tuple[int, int], red_tiles: list[tuple[int, int]]) -> bool:
    """Check if a point is inside or on the boundary of the polygon.

    Uses ray casting algorithm for rectilinear polygons.

    Args:
        point: (x, y) point to check
        red_tiles: List of red tile positions defining the polygon

    Returns:
        True if point is inside or on boundary
    """
    x, y = point
    n = len(red_tiles)

    # Check if point is on any edge
    for i in range(n):
        p1 = red_tiles[i]
        p2 = red_tiles[(i + 1) % n]

        if p1[0] == p2[0]:  # Vertical edge
            if x == p1[0] and min(p1[1], p2[1]) <= y <= max(p1[1], p2[1]):
                return True
        else:  # Horizontal edge
            if y == p1[1] and min(p1[0], p2[0]) <= x <= max(p1[0], p2[0]):
                return True

    # Ray casting: count crossings to the right
    crossings = 0
    for i in range(n):
        p1 = red_tiles[i]
        p2 = red_tiles[(i + 1) % n]

        # Only vertical edges can be crossed by horizontal ray
        if p1[0] == p2[0]:
            edge_x = p1[0]
            y1, y2 = min(p1[1], p2[1]), max(p1[1], p2[1])
            # Ray goes to the right from point
            if edge_x > x and y1 < y <= y2:
                crossings += 1

    return crossings % 2 == 1


def segments_intersect_interior(
    ax1: int, ay1: int, ax2: int, ay2: int, bx1: int, by1: int, bx2: int, by2: int
) -> bool:
    """Check if two axis-aligned segments intersect in their interiors.

    Args:
        Segment A: (ax1,ay1) to (ax2,ay2)
        Segment B: (bx1,by1) to (bx2,by2)

    Returns:
        True if segments cross in interior (not just touch at endpoints)
    """
    # Normalize so that first coord <= second coord
    if ax1 > ax2:
        ax1, ax2 = ax2, ax1
    if ay1 > ay2:
        ay1, ay2 = ay2, ay1
    if bx1 > bx2:
        bx1, bx2 = bx2, bx1
    if by1 > by2:
        by1, by2 = by2, by1

    # Both horizontal
    if ay1 == ay2 and by1 == by2:
        if ay1 != by1:
            return False
        # Same y, check x overlap in interior
        return ax1 < bx2 and bx1 < ax2

    # Both vertical
    if ax1 == ax2 and bx1 == bx2:
        if ax1 != bx1:
            return False
        # Same x, check y overlap in interior
        return ay1 < by2 and by1 < ay2

    # One horizontal, one vertical
    if ay1 == ay2:  # A is horizontal, B is vertical
        # A: y = ay1, x from ax1 to ax2
        # B: x = bx1, y from by1 to by2
        # Interior crossing: bx1 strictly between ax1 and ax2, ay1 strictly between by1 and by2
        return ax1 < bx1 < ax2 and by1 < ay1 < by2
    else:  # A is vertical, B is horizontal
        # A: x = ax1, y from ay1 to ay2
        # B: y = by1, x from bx1 to bx2
        return bx1 < ax1 < bx2 and ay1 < by1 < ay2


def rectangle_valid(
    p1: tuple[int, int],
    p2: tuple[int, int],
    red_tiles: list[tuple[int, int]],
    edges: list[tuple[tuple[int, int], tuple[int, int]]],
) -> bool:
    """Check if rectangle with red tiles at opposite corners is valid.

    A rectangle is valid if all its tiles are inside the polygon.

    Args:
        p1: First red corner
        p2: Second red corner (opposite)
        red_tiles: List of all red tiles
        edges: Polygon edges

    Returns:
        True if rectangle is valid
    """
    x1, x2 = min(p1[0], p2[0]), max(p1[0], p2[0])
    y1, y2 = min(p1[1], p2[1]), max(p1[1], p2[1])

    # Check all 4 corners are inside or on polygon
    corners = [(x1, y1), (x1, y2), (x2, y1), (x2, y2)]
    for corner in corners:
        if not point_in_polygon(corner, red_tiles):
            return False

    # Check no polygon edge crosses the rectangle interior
    for edge in edges:
        ex1, ey1 = edge[0]
        ex2, ey2 = edge[1]

        # Check if polygon edge crosses rectangle interior
        # An edge crossing interior means part of the polygon boundary
        # goes through the rectangle, which would exclude tiles

        # First check if edge intersects rectangle interior
        # (not just touches the boundary)
        if ex1 == ex2:  # Vertical edge
            # Does this vertical line pass through rectangle interior?
            if x1 < ex1 < x2:  # Edge x is strictly inside rect x range
                # Does the edge's y range overlap with rect's y range?
                ey_min, ey_max = min(ey1, ey2), max(ey1, ey2)
                if ey_min < y2 and ey_max > y1:  # Y ranges overlap
                    # This edge passes through rectangle interior
                    return False
        else:  # Horizontal edge
            if y1 < ey1 < y2:  # Edge y is strictly inside rect y range
                ex_min, ex_max = min(ex1, ex2), max(ex1, ex2)
                if ex_min < x2 and ex_max > x1:  # X ranges overlap
                    return False

    return True


def parse_tiles(data: str) -> list[tuple[int, int]]:
    """Parse red tile positions from input.

    Args:
        data: The puzzle input

    Returns:
        List of (x, y) positions of red tiles
    """
    tiles = []
    for line in data.strip().split("\n"):
        x, y = line.split(",")
        tiles.append((int(x), int(y)))
    return tiles


def rectangle_area(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    """Calculate the area of a rectangle with opposite corners at p1 and p2.

    The area includes the boundary tiles, so a rectangle from (2,5) to (9,7)
    has width 8 (columns 2-9 inclusive) and height 3 (rows 5-7 inclusive).

    Args:
        p1: First corner (x, y)
        p2: Opposite corner (x, y)

    Returns:
        Area of the rectangle (including boundary tiles)
    """
    width = abs(p2[0] - p1[0]) + 1
    height = abs(p2[1] - p1[1]) + 1
    return width * height


def part1(data: str) -> int:
    """Solve part 1 of the puzzle.

    Find the largest rectangle area using two red tiles as opposite corners.

    Args:
        data: The puzzle input

    Returns:
        The largest rectangle area
    """
    tiles = parse_tiles(data)
    max_area = 0

    for p1, p2 in combinations(tiles, 2):
        area = rectangle_area(p1, p2)
        max_area = max(max_area, area)

    return max_area


def part2(data: str) -> int:
    """Solve part 2 of the puzzle.

    Find the largest rectangle with red corners that only contains red/green tiles.

    Args:
        data: The puzzle input

    Returns:
        The largest valid rectangle area
    """
    tiles = parse_tiles(data)
    edges = get_polygon_edges(tiles)
    max_area = 0

    for p1, p2 in combinations(tiles, 2):
        if rectangle_valid(p1, p2, tiles, edges):
            area = rectangle_area(p1, p2)
            max_area = max(max_area, area)

    return max_area


def run() -> None:
    """Run the day 9 solutions."""
    print("Day 9: Movie Theater")

    data = get_input(9)

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    run()
