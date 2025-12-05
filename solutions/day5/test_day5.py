"""Tests for Day 5: Cafeteria."""

from solutions.day5.day5 import (
    count_fresh_ids,
    is_fresh,
    merge_ranges,
    parse_input,
    part1,
    part2,
)

EXAMPLE_INPUT = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""


class TestParseInput:
    """Tests for parse_input function."""

    def test_example(self) -> None:
        """Parse example input correctly."""
        ranges, ingredients = parse_input(EXAMPLE_INPUT)
        assert ranges == [(3, 5), (10, 14), (16, 20), (12, 18)]
        assert ingredients == [1, 5, 8, 11, 17, 32]


class TestIsFresh:
    """Tests for is_fresh function."""

    def test_in_range(self) -> None:
        """Ingredient in a range is fresh."""
        ranges = [(3, 5), (10, 14)]
        assert is_fresh(4, ranges) is True

    def test_at_range_start(self) -> None:
        """Ingredient at range start is fresh."""
        ranges = [(3, 5)]
        assert is_fresh(3, ranges) is True

    def test_at_range_end(self) -> None:
        """Ingredient at range end is fresh."""
        ranges = [(3, 5)]
        assert is_fresh(5, ranges) is True

    def test_not_in_range(self) -> None:
        """Ingredient not in any range is spoiled."""
        ranges = [(3, 5), (10, 14)]
        assert is_fresh(8, ranges) is False

    def test_in_overlapping_ranges(self) -> None:
        """Ingredient in overlapping ranges is fresh."""
        ranges = [(10, 14), (12, 18)]
        assert is_fresh(13, ranges) is True


class TestPart1:
    """Tests for part1 function."""

    def test_example(self) -> None:
        """Example from puzzle gives 3."""
        assert part1(EXAMPLE_INPUT) == 3


class TestMergeRanges:
    """Tests for merge_ranges function."""

    def test_no_overlap(self) -> None:
        """Non-overlapping ranges stay separate."""
        ranges = [(1, 3), (5, 7)]
        assert merge_ranges(ranges) == [(1, 3), (5, 7)]

    def test_overlap(self) -> None:
        """Overlapping ranges are merged."""
        ranges = [(1, 5), (3, 7)]
        assert merge_ranges(ranges) == [(1, 7)]

    def test_adjacent(self) -> None:
        """Adjacent ranges are merged."""
        ranges = [(1, 3), (4, 6)]
        assert merge_ranges(ranges) == [(1, 6)]

    def test_contained(self) -> None:
        """Contained range is absorbed."""
        ranges = [(1, 10), (3, 5)]
        assert merge_ranges(ranges) == [(1, 10)]

    def test_example(self) -> None:
        """Example ranges merge correctly."""
        ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
        # 10-14 and 12-18 overlap -> 10-18
        # 16-20 overlaps with 10-18 -> 10-20
        assert merge_ranges(ranges) == [(3, 5), (10, 20)]


class TestCountFreshIds:
    """Tests for count_fresh_ids function."""

    def test_example(self) -> None:
        """Example ranges give 14 fresh IDs."""
        ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
        # 3-5 = 3 IDs, 10-20 = 11 IDs -> 14 total
        assert count_fresh_ids(ranges) == 14


class TestPart2:
    """Tests for part2 function."""

    def test_example(self) -> None:
        """Example from puzzle gives 14."""
        assert part2(EXAMPLE_INPUT) == 14
