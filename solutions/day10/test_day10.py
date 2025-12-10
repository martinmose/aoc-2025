"""Tests for Day 10: Factory."""

from solutions.day10.day10 import (
    parse_machine,
    parse_machine_part2,
    part1,
    part2,
    solve_machine,
    solve_machine_part2,
)

EXAMPLE_INPUT = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""


class TestParseMachine:
    """Tests for parse_machine function."""

    def test_parse_first_machine(self) -> None:
        """Test parsing first example machine."""
        line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
        target, buttons = parse_machine(line)
        assert target == [False, True, True, False]
        assert len(buttons) == 6
        assert buttons[0] == [3]
        assert buttons[1] == [1, 3]
        assert buttons[5] == [0, 1]

    def test_parse_third_machine(self) -> None:
        """Test parsing third example machine."""
        line = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
        target, buttons = parse_machine(line)
        assert target == [False, True, True, True, False, True]
        assert len(buttons) == 4


class TestSolveMachine:
    """Tests for solve_machine function."""

    def test_first_machine(self) -> None:
        """Test solving first example machine."""
        target = [False, True, True, False]
        buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
        assert solve_machine(target, buttons) == 2

    def test_second_machine(self) -> None:
        """Test solving second example machine."""
        target = [False, False, False, True, False]
        buttons = [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]
        assert solve_machine(target, buttons) == 3

    def test_third_machine(self) -> None:
        """Test solving third example machine."""
        target = [False, True, True, True, False, True]
        buttons = [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]
        assert solve_machine(target, buttons) == 2


class TestPart1:
    """Tests for part1 function."""

    def test_example(self) -> None:
        """Test part 1 with example input."""
        result = part1(EXAMPLE_INPUT)
        assert result == 7


class TestParseMachinePart2:
    """Tests for parse_machine_part2 function."""

    def test_parse_first_machine(self) -> None:
        """Test parsing first example machine for part 2."""
        line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
        target, buttons = parse_machine_part2(line)
        assert target == [3, 5, 4, 7]
        assert len(buttons) == 6


class TestSolveMachinePart2:
    """Tests for solve_machine_part2 function."""

    def test_first_machine(self) -> None:
        """Test solving first example machine for part 2."""
        target = [3, 5, 4, 7]
        buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
        assert solve_machine_part2(target, buttons) == 10

    def test_second_machine(self) -> None:
        """Test solving second example machine for part 2."""
        target = [7, 5, 12, 7, 2]
        buttons = [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]
        assert solve_machine_part2(target, buttons) == 12

    def test_third_machine(self) -> None:
        """Test solving third example machine for part 2."""
        target = [10, 11, 11, 5, 10, 5]
        buttons = [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]
        assert solve_machine_part2(target, buttons) == 11


class TestPart2:
    """Tests for part2 function."""

    def test_example(self) -> None:
        """Test part 2 with example input."""
        result = part2(EXAMPLE_INPUT)
        assert result == 33
