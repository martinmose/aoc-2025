"""Tests for Day 2: Gift Shop."""

from solutions.day2.day2 import is_repeated_sequence, part1, part2

EXAMPLE_INPUT = """\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
"""


class TestIsRepeatedSequence:
    """Tests for is_repeated_sequence function."""

    def test_single_digit_repeated(self) -> None:
        """Test single digit repeated twice."""
        assert is_repeated_sequence(11) is True
        assert is_repeated_sequence(22) is True
        assert is_repeated_sequence(99) is True

    def test_two_digits_repeated(self) -> None:
        """Test two digit sequence repeated."""
        assert is_repeated_sequence(6464) is True
        assert is_repeated_sequence(1010) is True

    def test_three_digits_repeated(self) -> None:
        """Test three digit sequence repeated."""
        assert is_repeated_sequence(123123) is True
        assert is_repeated_sequence(446446) is True

    def test_not_repeated(self) -> None:
        """Test numbers that are not repeated sequences."""
        assert is_repeated_sequence(12) is False
        assert is_repeated_sequence(101) is False
        assert is_repeated_sequence(1234) is False

    def test_large_numbers(self) -> None:
        """Test large repeated sequences."""
        assert is_repeated_sequence(1188511885) is True
        assert is_repeated_sequence(222222) is True

    def test_more_than_two_repeats(self) -> None:
        """Test sequences repeated more than twice."""
        assert is_repeated_sequence(111) is True  # 1 repeated 3 times
        assert is_repeated_sequence(999) is True  # 9 repeated 3 times
        assert is_repeated_sequence(123123123) is True  # 123 repeated 3 times
        assert is_repeated_sequence(1212121212) is True  # 12 repeated 5 times
        assert is_repeated_sequence(1111111) is True  # 1 repeated 7 times

    def test_part2_specific_cases(self) -> None:
        """Test specific cases from part 2 examples."""
        assert is_repeated_sequence(565656) is True  # 56 repeated 3 times
        assert is_repeated_sequence(824824824) is True  # 824 repeated 3 times
        assert is_repeated_sequence(2121212121) is True  # 21 repeated 5 times


class TestPart1:
    """Tests for part 1."""

    def test_example(self) -> None:
        """Test with example from the puzzle description."""
        assert part1(EXAMPLE_INPUT) == 1227775554


class TestPart2:
    """Tests for part 2."""

    def test_example(self) -> None:
        """Test with example from the puzzle description."""
        assert part2(EXAMPLE_INPUT) == 4174379265
