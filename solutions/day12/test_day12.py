"""Tests for Day 12: Christmas Tree Farm."""

from solutions.day12.day12 import part1

EXAMPLE_INPUT = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""


class TestPart1:
    """Tests for Part 1."""

    def test_example(self) -> None:
        """Test with the example from the problem description."""
        assert part1(EXAMPLE_INPUT) == 2
