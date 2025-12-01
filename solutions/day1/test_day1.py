"""Tests for Day 1: Secret Entrance."""

from solutions.day1.day1 import part1, part2


EXAMPLE_INPUT = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""


class TestPart1:
    """Tests for part 1."""

    def test_example(self) -> None:
        """Test with example from the puzzle description."""
        assert part1(EXAMPLE_INPUT) == 3


class TestPart2:
    """Tests for part 2."""

    def test_example(self) -> None:
        """Test with example from the puzzle description."""
        assert part2(EXAMPLE_INPUT) == 6

    def test_full_rotation(self) -> None:
        """Test R1000 from position 50 crosses 0 ten times."""
        # From 50, R1000 should cross 0 exactly 10 times and end at 50
        assert part2("R1000") == 10
