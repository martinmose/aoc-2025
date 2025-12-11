"""Day 11: Reactor - Advent of Code 2025."""

from functools import cache

from solutions.utils import get_input


def parse_graph(data: str) -> dict[str, list[str]]:
    """Parse the device connections into a graph.

    Args:
        data: The puzzle input

    Returns:
        Dictionary mapping device names to their output devices
    """
    graph: dict[str, list[str]] = {}
    for line in data.strip().split("\n"):
        parts = line.split(": ")
        device = parts[0]
        outputs = parts[1].split() if len(parts) > 1 else []
        graph[device] = outputs
    return graph


def count_paths(graph: dict[str, list[str]], start: str, end: str) -> int:
    """Count all paths from start to end in the graph.

    Uses memoization to efficiently count paths.

    Args:
        graph: The device connection graph
        start: Starting device
        end: Target device

    Returns:
        Number of distinct paths from start to end
    """
    # Convert to tuple for hashing in cache
    graph_tuple = tuple((k, tuple(v)) for k, v in sorted(graph.items()))

    @cache
    def count_from(node: str, graph_key: tuple[tuple[str, tuple[str, ...]], ...]) -> int:
        if node == end:
            return 1
        if node not in graph:
            return 0

        total = 0
        for neighbor in graph[node]:
            total += count_from(neighbor, graph_key)
        return total

    return count_from(start, graph_tuple)


def part1(data: str) -> int:
    """Solve part 1 of the puzzle.

    Count all paths from 'you' to 'out'.

    Args:
        data: The puzzle input

    Returns:
        Number of distinct paths
    """
    graph = parse_graph(data)
    return count_paths(graph, "you", "out")


def count_paths_through(
    graph: dict[str, list[str]], start: str, end: str, required: set[str]
) -> int:
    """Count paths from start to end that pass through all required nodes.

    Args:
        graph: The device connection graph
        start: Starting device
        end: Target device
        required: Set of nodes that must be visited

    Returns:
        Number of distinct paths that visit all required nodes
    """
    # Use a frozenset to track which required nodes have been visited
    # State: (current_node, visited_required)

    @cache
    def count_from(node: str, visited: frozenset[str]) -> int:
        # Update visited if current node is required
        if node in required:
            visited = visited | {node}

        if node == end:
            # Only count if all required nodes were visited
            return 1 if visited == required else 0

        if node not in graph:
            return 0

        total = 0
        for neighbor in graph[node]:
            total += count_from(neighbor, visited)
        return total

    return count_from(start, frozenset())


def part2(data: str) -> int:
    """Solve part 2 of the puzzle.

    Count paths from 'svr' to 'out' that visit both 'dac' and 'fft'.

    Args:
        data: The puzzle input

    Returns:
        Number of distinct paths visiting both dac and fft
    """
    graph = parse_graph(data)
    return count_paths_through(graph, "svr", "out", {"dac", "fft"})


def run() -> None:
    """Run the day 11 solutions."""
    print("Day 11: Reactor")

    data = get_input(11)

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    run()
