"""Tests for Day 4: Printing Department."""

from solutions.day4.day4 import count_adjacent_rolls, find_accessible_rolls, part1, part2

EXAMPLE_INPUT = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""


class TestCountAdjacentRolls:
    """Tests for count_adjacent_rolls function."""

    def test_corner_roll(self) -> None:
        """Roll in corner has limited neighbors."""
        grid = ["@.", ".."]
        assert count_adjacent_rolls(grid, 0, 0) == 0

    def test_surrounded_roll(self) -> None:
        """Roll surrounded by rolls has 8 neighbors."""
        grid = ["@@@", "@@@", "@@@"]
        assert count_adjacent_rolls(grid, 1, 1) == 8

    def test_partial_neighbors(self) -> None:
        """Roll with some neighbors."""
        grid = ["@.@", ".@.", "@.@"]
        assert count_adjacent_rolls(grid, 1, 1) == 4


class TestFindAccessibleRolls:
    """Tests for find_accessible_rolls function."""

    def test_example(self) -> None:
        """Example from puzzle gives 13 accessible rolls."""
        grid = EXAMPLE_INPUT.split("\n")
        assert len(find_accessible_rolls(grid)) == 13


class TestPart1:
    """Tests for part1 function."""

    def test_example(self) -> None:
        """Example from puzzle gives 13."""
        assert part1(EXAMPLE_INPUT) == 13


class TestPart2:
    """Tests for part2 function."""

    def test_example(self) -> None:
        """Example from puzzle gives 43 total rolls removed."""
        assert part2(EXAMPLE_INPUT) == 43
