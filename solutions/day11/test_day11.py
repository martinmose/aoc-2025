"""Tests for Day 11: Reactor."""

from solutions.day11.day11 import count_paths, count_paths_through, parse_graph, part1, part2

EXAMPLE_INPUT = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

EXAMPLE_INPUT_2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""


class TestParseGraph:
    """Tests for parse_graph function."""

    def test_example(self) -> None:
        """Parse example graph correctly."""
        graph = parse_graph(EXAMPLE_INPUT)
        assert graph["you"] == ["bbb", "ccc"]
        assert graph["bbb"] == ["ddd", "eee"]
        assert graph["ccc"] == ["ddd", "eee", "fff"]


class TestCountPaths:
    """Tests for count_paths function."""

    def test_simple(self) -> None:
        """Simple linear path."""
        graph = {"a": ["b"], "b": ["c"]}
        assert count_paths(graph, "a", "c") == 1

    def test_fork(self) -> None:
        """Path with a fork."""
        graph = {"a": ["b", "c"], "b": ["d"], "c": ["d"]}
        assert count_paths(graph, "a", "d") == 2


class TestPart1:
    """Tests for part1 function."""

    def test_example(self) -> None:
        """Example from puzzle gives 5 paths."""
        assert part1(EXAMPLE_INPUT) == 5


class TestCountPathsThrough:
    """Tests for count_paths_through function."""

    def test_all_paths(self) -> None:
        """Total paths from svr to out is 8."""
        graph = parse_graph(EXAMPLE_INPUT_2)
        assert count_paths(graph, "svr", "out") == 8

    def test_through_both(self) -> None:
        """Only 2 paths visit both dac and fft."""
        graph = parse_graph(EXAMPLE_INPUT_2)
        assert count_paths_through(graph, "svr", "out", {"dac", "fft"}) == 2


class TestPart2:
    """Tests for part2 function."""

    def test_example(self) -> None:
        """Example from puzzle gives 2 paths."""
        assert part2(EXAMPLE_INPUT_2) == 2
