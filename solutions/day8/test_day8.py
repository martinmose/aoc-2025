"""Tests for Day 8: Playground."""

from solutions.day8.day8 import (
    connect_closest_pairs,
    distance,
    find_final_connection,
    parse_positions,
    part1,
    part2,
)

EXAMPLE_INPUT = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""


class TestParsePositions:
    """Tests for parse_positions function."""

    def test_example(self) -> None:
        """Parse example positions correctly."""
        positions = parse_positions(EXAMPLE_INPUT)
        assert len(positions) == 20
        assert positions[0] == (162, 817, 812)
        assert positions[-1] == (425, 690, 689)


class TestDistance:
    """Tests for distance function."""

    def test_same_point(self) -> None:
        """Distance to same point is 0."""
        assert distance((0, 0, 0), (0, 0, 0)) == 0

    def test_simple_distance(self) -> None:
        """Simple 3D distance calculation."""
        # 3-4-5 triangle extended to 3D
        assert distance((0, 0, 0), (3, 4, 0)) == 5.0


class TestConnectClosestPairs:
    """Tests for connect_closest_pairs function."""

    def test_example_10_connections(self) -> None:
        """After 10 connections, largest circuits are 5, 4, 2."""
        positions = parse_positions(EXAMPLE_INPUT)
        sizes = connect_closest_pairs(positions, 10)
        # 11 circuits: one 5, one 4, two 2s, seven 1s
        assert sizes[0] == 5
        assert sizes[1] == 4
        assert sizes[2] == 2


class TestPart1:
    """Tests for part1 function."""

    def test_example(self) -> None:
        """Example with 10 connections gives 5 * 4 * 2 = 40."""
        assert part1(EXAMPLE_INPUT, num_connections=10) == 40


class TestFindFinalConnection:
    """Tests for find_final_connection function."""

    def test_example(self) -> None:
        """Final connection is between 216,146,977 and 117,168,530."""
        positions = parse_positions(EXAMPLE_INPUT)
        p1, p2 = find_final_connection(positions)
        # The two positions (order may vary)
        expected = {(216, 146, 977), (117, 168, 530)}
        assert {p1, p2} == expected


class TestPart2:
    """Tests for part2 function."""

    def test_example(self) -> None:
        """Example gives 216 * 117 = 25272."""
        assert part2(EXAMPLE_INPUT) == 25272
