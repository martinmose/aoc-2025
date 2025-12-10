"""Tests for Day 9: Movie Theater."""

import pytest

from solutions.day9.day9 import parse_tiles, part1, part2, point_in_polygon, rectangle_area

EXAMPLE_INPUT = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""


class TestParseTiles:
    """Tests for parse_tiles function."""

    def test_parse_example(self) -> None:
        """Test parsing example input."""
        tiles = parse_tiles(EXAMPLE_INPUT)
        assert len(tiles) == 8
        assert tiles[0] == (7, 1)
        assert tiles[1] == (11, 1)
        assert tiles[2] == (11, 7)


class TestRectangleArea:
    """Tests for rectangle_area function."""

    def test_area_24(self) -> None:
        """Test rectangle from (2,5) to (9,7) = 7 * (7-5) = 7*2 = 14... wait.

        Actually looking at the problem: width = 9-2 = 7, height = 7-5 = 2, but
        the problem says area 24. Let me re-read...

        Ah, the rectangle includes the tiles, so width = 9-2+1 = 8, height = 7-5+1 = 3.
        8 * 3 = 24. So we need to add 1 to each dimension.
        """
        # Actually, re-reading: width*height using inclusive dimensions
        # From 2 to 9 inclusive = 8 tiles wide
        # From 5 to 7 inclusive = 3 tiles high
        # But wait, looking at the visual, it seems like the area is just
        # the rectangle area with the corners, which would be (9-2)*(7-5) = 7*2 = 14
        # but they say 24...
        #
        # Looking at the visual again - the O's span from column 2 to 9 (8 columns)
        # and rows 5 to 7 (3 rows). So it's 8*3 = 24.
        # This means area = (|x2-x1|+1) * (|y2-y1|+1)
        pass

    def test_area_basic(self) -> None:
        """Test basic area calculation."""
        # Line on same row: 6 columns * 1 row = 6
        assert rectangle_area((0, 0), (5, 0)) == 6
        # Line on same column: 1 column * 6 rows = 6
        assert rectangle_area((0, 0), (0, 5)) == 6
        # Example from problem: (2,5) to (9,7) = 8*3 = 24
        assert rectangle_area((2, 5), (9, 7)) == 24


class TestPart1:
    """Tests for part1 function."""

    def test_example(self) -> None:
        """Test part 1 with example input."""
        result = part1(EXAMPLE_INPUT)
        assert result == 50


class TestPointInPolygon:
    """Tests for point_in_polygon function."""

    def test_example_polygon(self) -> None:
        """Test point in polygon for example."""
        tiles = parse_tiles(EXAMPLE_INPUT)

        # Red tiles should be in the polygon (on boundary)
        assert point_in_polygon((7, 1), tiles)
        assert point_in_polygon((11, 1), tiles)
        assert point_in_polygon((2, 5), tiles)

        # Green tiles on edges should be in the polygon
        assert point_in_polygon((8, 1), tiles)  # Between (7,1) and (11,1)
        assert point_in_polygon((11, 5), tiles)  # Between (11,1) and (11,7)

        # Interior tiles should be in the polygon
        assert point_in_polygon((8, 3), tiles)  # Inside the polygon

        # Tiles outside should NOT be in the polygon
        assert not point_in_polygon((0, 0), tiles)
        assert not point_in_polygon((1, 1), tiles)


class TestPart2:
    """Tests for part2 function."""

    def test_example(self) -> None:
        """Test part 2 with example input."""
        result = part2(EXAMPLE_INPUT)
        assert result == 24
