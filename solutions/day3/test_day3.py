"""Tests for Day 3: Lobby."""

from solutions.day3.day3 import max_joltage, part1, part2

EXAMPLE_INPUT = """987654321111111
811111111111119
234234234234278
818181911112111"""


class TestMaxJoltage:
    """Tests for max_joltage function."""

    def test_example_1(self) -> None:
        """First two batteries give 98."""
        assert max_joltage("987654321111111") == 98

    def test_example_2(self) -> None:
        """8 and 9 at ends give 89."""
        assert max_joltage("811111111111119") == 89

    def test_example_3(self) -> None:
        """Last two batteries give 78."""
        assert max_joltage("234234234234278") == 78

    def test_example_4(self) -> None:
        """9 followed by 2 gives 92."""
        assert max_joltage("818181911112111") == 92

    def test_simple(self) -> None:
        """Simple two digit case."""
        assert max_joltage("12") == 12

    def test_reversed(self) -> None:
        """Must maintain order, so 21 -> 21."""
        assert max_joltage("21") == 21


class TestPart1:
    """Tests for part1 function."""

    def test_example(self) -> None:
        """Example from puzzle gives 357."""
        assert part1(EXAMPLE_INPUT) == 357


class TestMaxJoltage12:
    """Tests for max_joltage with 12 batteries."""

    def test_example_1(self) -> None:
        """Everything except some 1s at the end."""
        assert max_joltage("987654321111111", 12) == 987654321111

    def test_example_2(self) -> None:
        """Everything except some 1s."""
        assert max_joltage("811111111111119", 12) == 811111111119

    def test_example_3(self) -> None:
        """Skip 2, 3, 2 near the start."""
        assert max_joltage("234234234234278", 12) == 434234234278

    def test_example_4(self) -> None:
        """Skip some 1s near the front."""
        assert max_joltage("818181911112111", 12) == 888911112111


class TestPart2:
    """Tests for part2 function."""

    def test_example(self) -> None:
        """Example from puzzle gives 3121910778619."""
        assert part2(EXAMPLE_INPUT) == 3121910778619
