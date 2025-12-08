"""Tests for Day 7: Laboratories."""

from solutions.day7.day7 import count_timelines, part1, part2, simulate_beams

EXAMPLE_INPUT = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""


class TestSimulateBeams:
    """Tests for simulate_beams function."""

    def test_simple_split(self) -> None:
        """Single splitter causes one split."""
        data = """S
^"""
        assert simulate_beams(data) == 1

    def test_no_splitter(self) -> None:
        """No splitters means no splits."""
        data = """S
.
."""
        assert simulate_beams(data) == 0

    def test_two_splits(self) -> None:
        """Two sequential splitters."""
        data = """.S.
...
.^.
...
^.^"""
        assert simulate_beams(data) == 3  # 1 split at first ^, 2 splits at bottom ^s


class TestPart1:
    """Tests for part1 function."""

    def test_example(self) -> None:
        """Example from puzzle gives 21 splits."""
        assert part1(EXAMPLE_INPUT) == 21


class TestCountTimelines:
    """Tests for count_timelines function."""

    def test_no_splitter(self) -> None:
        """No splitters means 1 timeline."""
        data = """S
.
."""
        assert count_timelines(data) == 1

    def test_single_split(self) -> None:
        """Single splitter creates 2 timelines (if both paths are valid)."""
        data = """.S.
.^."""
        assert count_timelines(data) == 2

    def test_two_sequential_splits(self) -> None:
        """Two sequential splitters create 4 timelines."""
        data = """..S..
.....
..^..
.....
.^.^."""
        assert count_timelines(data) == 4  # 1 -> 2 -> 4


class TestPart2:
    """Tests for part2 function."""

    def test_example(self) -> None:
        """Example from puzzle gives 40 timelines."""
        assert part2(EXAMPLE_INPUT) == 40
