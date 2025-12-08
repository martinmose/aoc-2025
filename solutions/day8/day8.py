"""Day 8: Playground - Advent of Code 2025."""

import math
from collections.abc import Iterator

from solutions.utils import get_input


def parse_positions(data: str) -> list[tuple[int, int, int]]:
    """Parse junction box positions from input.

    Args:
        data: The puzzle input

    Returns:
        List of (x, y, z) positions
    """
    positions = []
    for line in data.strip().split("\n"):
        x, y, z = line.split(",")
        positions.append((int(x), int(y), int(z)))
    return positions


def distance(p1: tuple[int, int, int], p2: tuple[int, int, int]) -> float:
    """Calculate Euclidean distance between two 3D points.

    Args:
        p1: First point (x, y, z)
        p2: Second point (x, y, z)

    Returns:
        Straight-line distance
    """
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)


def all_pairs_by_distance(
    positions: list[tuple[int, int, int]],
) -> Iterator[tuple[float, int, int]]:
    """Generate all pairs of positions sorted by distance.

    Args:
        positions: List of positions

    Yields:
        Tuples of (distance, index1, index2) sorted by distance
    """
    pairs = []
    n = len(positions)
    for i in range(n):
        for j in range(i + 1, n):
            d = distance(positions[i], positions[j])
            pairs.append((d, i, j))
    pairs.sort()
    yield from pairs


class UnionFind:
    """Union-Find data structure for tracking connected components."""

    def __init__(self, n: int) -> None:
        """Initialize with n separate components.

        Args:
            n: Number of elements
        """
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n

    def find(self, x: int) -> int:
        """Find the root of element x with path compression.

        Args:
            x: Element to find

        Returns:
            Root of the component containing x
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Union two elements.

        Args:
            x: First element
            y: Second element

        Returns:
            True if elements were in different components, False otherwise
        """
        px, py = self.find(x), self.find(y)
        if px == py:
            return False

        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

    def get_component_sizes(self) -> list[int]:
        """Get sizes of all components.

        Returns:
            List of component sizes, sorted descending
        """
        sizes = []
        for i in range(len(self.parent)):
            if self.find(i) == i:
                sizes.append(self.size[i])
        return sorted(sizes, reverse=True)


def connect_closest_pairs(positions: list[tuple[int, int, int]], num_connections: int) -> list[int]:
    """Connect the closest pairs of junction boxes.

    Args:
        positions: List of junction box positions
        num_connections: Number of connection attempts to make

    Returns:
        List of component sizes after making connections
    """
    uf = UnionFind(len(positions))

    for connections_attempted, (_, i, j) in enumerate(all_pairs_by_distance(positions)):
        # Try to connect even if already in same circuit
        uf.union(i, j)
        if connections_attempted + 1 >= num_connections:
            break

    return uf.get_component_sizes()


def part1(data: str, num_connections: int = 1000) -> int:
    """Solve part 1 of the puzzle.

    Connect the closest pairs and return product of 3 largest circuit sizes.

    Args:
        data: The puzzle input
        num_connections: Number of connections to make

    Returns:
        Product of three largest circuit sizes
    """
    positions = parse_positions(data)
    sizes = connect_closest_pairs(positions, num_connections)
    return sizes[0] * sizes[1] * sizes[2]


def find_final_connection(
    positions: list[tuple[int, int, int]],
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """Find the connection that unifies all junction boxes into one circuit.

    Args:
        positions: List of junction box positions

    Returns:
        Tuple of the two positions that form the final connection
    """
    n = len(positions)
    uf = UnionFind(n)
    num_components = n

    for _, i, j in all_pairs_by_distance(positions):
        if uf.union(i, j):
            num_components -= 1
            if num_components == 1:
                return positions[i], positions[j]

    # Should not reach here if there are at least 2 positions
    return positions[0], positions[0]


def part2(data: str) -> int:
    """Solve part 2 of the puzzle.

    Find the last connection needed to unify all circuits, return product of X coords.

    Args:
        data: The puzzle input

    Returns:
        Product of X coordinates of the final two connected junction boxes
    """
    positions = parse_positions(data)
    p1, p2 = find_final_connection(positions)
    return p1[0] * p2[0]


def run() -> None:
    """Run the day 8 solutions."""
    print("Day 8: Playground")

    data = get_input(8)

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    run()
