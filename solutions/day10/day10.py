"""Day 10: Factory - Advent of Code 2025."""

import re
from itertools import product

from solutions.utils import get_input


def parse_machine(line: str) -> tuple[list[bool], list[list[int]]]:
    """Parse a machine specification for part 1.

    Args:
        line: A line from the puzzle input

    Returns:
        Tuple of (target pattern as list of bools, list of button toggles)
    """
    # Extract indicator light diagram [.##.]
    diagram_match = re.search(r"\[([.#]+)\]", line)
    if not diagram_match:
        raise ValueError(f"No diagram found in line: {line}")
    diagram = diagram_match.group(1)
    target = [c == "#" for c in diagram]

    # Extract button wiring schematics (0,2,3) etc
    buttons = []
    for match in re.finditer(r"\(([0-9,]+)\)", line):
        indices = [int(x) for x in match.group(1).split(",")]
        buttons.append(indices)

    return target, buttons


def parse_machine_part2(line: str) -> tuple[list[int], list[list[int]]]:
    """Parse a machine specification for part 2.

    Args:
        line: A line from the puzzle input

    Returns:
        Tuple of (joltage requirements as list of ints, list of button indices)
    """
    # Extract joltage requirements {3,5,4,7}
    joltage_match = re.search(r"\{([0-9,]+)\}", line)
    if not joltage_match:
        raise ValueError(f"No joltage requirements found in line: {line}")
    joltage = [int(x) for x in joltage_match.group(1).split(",")]

    # Extract button wiring schematics (0,2,3) etc
    buttons = []
    for match in re.finditer(r"\(([0-9,]+)\)", line):
        indices = [int(x) for x in match.group(1).split(",")]
        buttons.append(indices)

    return joltage, buttons


def parse_input(data: str) -> list[tuple[list[bool], list[list[int]]]]:
    """Parse all machines from input.

    Args:
        data: The puzzle input

    Returns:
        List of (target, buttons) for each machine
    """
    machines = []
    for line in data.strip().split("\n"):
        machines.append(parse_machine(line))
    return machines


def solve_machine(target: list[bool], buttons: list[list[int]]) -> int:
    """Find minimum button presses to achieve target configuration.

    Since each button toggles (XOR), pressing twice cancels out.
    So each button is pressed 0 or 1 times.
    We try all 2^n combinations and find the one that works with fewest presses.

    Args:
        target: Target light pattern
        buttons: List of button toggle indices

    Returns:
        Minimum number of button presses needed
    """
    n_lights = len(target)
    n_buttons = len(buttons)

    # Convert buttons to bitmasks for efficiency
    button_masks = []
    for btn in buttons:
        mask = 0
        for idx in btn:
            if idx < n_lights:
                mask |= 1 << idx
        button_masks.append(mask)

    # Convert target to bitmask
    target_mask = 0
    for i, on in enumerate(target):
        if on:
            target_mask |= 1 << i

    # Try all combinations of button presses
    min_presses = float("inf")

    for combo in product([0, 1], repeat=n_buttons):
        # Calculate resulting light state
        state = 0
        presses = 0
        for i, pressed in enumerate(combo):
            if pressed:
                state ^= button_masks[i]
                presses += 1

        if state == target_mask and presses < min_presses:
            min_presses = presses

    return int(min_presses) if min_presses != float("inf") else -1


def part1(data: str) -> int:
    """Solve part 1 of the puzzle.

    Find the total minimum button presses for all machines.

    Args:
        data: The puzzle input

    Returns:
        Total minimum button presses
    """
    machines = parse_input(data)
    total = 0

    for target, buttons in machines:
        presses = solve_machine(target, buttons)
        total += presses

    return total


def solve_machine_part2(target: list[int], buttons: list[list[int]]) -> int:
    """Find minimum button presses to achieve target joltage configuration.

    This is an ILP problem: minimize sum(x) subject to Ax = b, x >= 0, x integer
    where A is the button-counter incidence matrix and b is the target.

    Uses Gaussian elimination to reduce the problem, then searches the reduced space.

    Args:
        target: Target joltage values for each counter
        buttons: List of button indices (which counters each button affects)

    Returns:
        Minimum number of button presses needed
    """
    from fractions import Fraction

    n_counters = len(target)
    n_buttons = len(buttons)

    if n_buttons == 0:
        return 0 if all(t == 0 for t in target) else -1

    # Build the augmented matrix [A | b] where A^T x = b
    matrix = []
    for i in range(n_counters):
        row = []
        for j in range(n_buttons):
            if i in buttons[j]:
                row.append(Fraction(1))
            else:
                row.append(Fraction(0))
        row.append(Fraction(target[i]))
        matrix.append(row)

    # Gaussian elimination to reduced row echelon form
    pivot_row = 0
    pivot_cols = []

    for col in range(n_buttons):
        pivot_found = None
        for row in range(pivot_row, n_counters):
            if matrix[row][col] != 0:
                pivot_found = row
                break

        if pivot_found is None:
            continue

        matrix[pivot_row], matrix[pivot_found] = matrix[pivot_found], matrix[pivot_row]

        scale = matrix[pivot_row][col]
        for c in range(n_buttons + 1):
            matrix[pivot_row][c] /= scale

        for row in range(n_counters):
            if row != pivot_row and matrix[row][col] != 0:
                factor = matrix[row][col]
                for c in range(n_buttons + 1):
                    matrix[row][c] -= factor * matrix[pivot_row][c]

        pivot_cols.append(col)
        pivot_row += 1

    # Check for inconsistency
    for row in range(pivot_row, n_counters):
        if matrix[row][n_buttons] != 0:
            return -1

    free_cols = [c for c in range(n_buttons) if c not in pivot_cols]

    # If no free variables, unique solution
    if not free_cols:
        solution = [Fraction(0)] * n_buttons
        for row, col in enumerate(pivot_cols):
            solution[col] = matrix[row][n_buttons]

        for s in solution:
            if s < 0 or s.denominator != 1:
                return -1
        return sum(int(s) for s in solution)

    # With free variables, express objective and constraints
    # x[pivot_col] = rhs[row] - sum(coef[row][free_col] * x[free_col])
    # Total = sum of all x = sum of pivot vars + sum of free vars
    #       = sum(rhs) - sum(coef * free) + sum(free)

    # Compute objective coefficients for free variables
    # obj = constant + sum(obj_coef[i] * free[i])
    obj_constant = Fraction(0)
    obj_coefs = [Fraction(1)] * len(free_cols)  # Each free var contributes 1 directly

    for row, _pivot_col in enumerate(pivot_cols):
        obj_constant += matrix[row][n_buttons]
        for i, free_col in enumerate(free_cols):
            # Pivot var contribution: -coef * free
            obj_coefs[i] -= matrix[row][free_col]

    # Now find minimum over non-negative integer free vars such that all pivot vars are non-negative integers
    # Constraint for each pivot var: rhs - sum(coef * free) >= 0 and integer

    def get_solution(free_vals: list[int]) -> list[int] | None:
        """Given values for free variables, compute full solution."""
        solution = [Fraction(0)] * n_buttons

        for i, col in enumerate(free_cols):
            solution[col] = Fraction(free_vals[i])

        for row, pivot_col in enumerate(pivot_cols):
            val = matrix[row][n_buttons]
            for i, free_col in enumerate(free_cols):
                val -= matrix[row][free_col] * free_vals[i]
            solution[pivot_col] = val

        for s in solution:
            if s < 0 or s.denominator != 1:
                return None

        return [int(s) for s in solution]

    # Search over free variable space
    import math

    max_target = max(target)

    def compute_bounds(idx: int, current: list[int]) -> tuple[int, int]:
        """Compute bounds for free variable at index idx given current assignment.

        When all prior free variables are assigned, we can compute exact bounds.
        """
        free_col = free_cols[idx]

        # Start with wide bounds - any free var value up to 2x max target should suffice
        lo, hi = 0, max_target * 3

        for row, _pivot_col in enumerate(pivot_cols):
            # Effective RHS after accounting for already-assigned free variables
            effective_rhs = matrix[row][n_buttons]
            for i in range(idx):
                effective_rhs -= matrix[row][free_cols[i]] * current[i]

            coef = matrix[row][free_col]

            # Check if any remaining free variables (after idx) affect this constraint
            has_remaining_free = False
            for j in range(idx + 1, len(free_cols)):
                if matrix[row][free_cols[j]] != 0:
                    has_remaining_free = True
                    break

            # Only apply tight bounds when this is the last free variable affecting
            # this constraint, or when we can guarantee the bound is valid
            if not has_remaining_free:
                if coef > 0:
                    # effective_rhs - coef * free >= 0 => free <= effective_rhs / coef
                    if effective_rhs >= 0:
                        upper = int(effective_rhs / coef)
                        hi = min(hi, upper)
                    else:
                        # No valid value for this var can satisfy constraint
                        return (1, 0)  # Invalid range
                elif coef < 0 and effective_rhs < 0:
                    # effective_rhs - coef * free >= 0 => free >= effective_rhs / coef
                    lower = math.ceil(float(-effective_rhs) / float(-coef))
                    lo = max(lo, lower)

        return (max(0, lo), max(lo, hi))

    # Search with dynamic bounds and objective-based pruning
    best = float("inf")

    def search(idx: int, current: list[int]) -> None:
        nonlocal best

        if idx == len(free_cols):
            sol = get_solution(current)
            if sol is not None:
                total = sum(sol)
                best = min(best, total)
            return

        lo, hi = compute_bounds(idx, current)
        if lo > hi:
            return  # No feasible values

        coef = float(obj_coefs[idx])

        # Compute current partial objective
        partial_obj = float(obj_constant)
        for i in range(idx):
            partial_obj += float(obj_coefs[i]) * current[i]

        # Check if any remaining variables have negative coefficients
        has_negative_remaining = any(obj_coefs[j] < 0 for j in range(idx + 1, len(free_cols)))

        if coef >= 0 and not has_negative_remaining:
            # Can prune: as val increases, objective increases, and no future var can decrease it
            for val in range(lo, hi + 1):
                test_obj = partial_obj + coef * val
                if test_obj >= best:
                    break
                search(idx + 1, [*current, val])
        elif coef >= 0:
            # Can't prune: future variables might decrease objective
            for val in range(lo, hi + 1):
                search(idx + 1, [*current, val])
        else:
            # Prefer larger values - as val increases, objective decreases
            for val in range(hi, lo - 1, -1):
                search(idx + 1, [*current, val])

    search(0, [])

    return int(best) if best != float("inf") else -1


def part2(data: str) -> int:
    """Solve part 2 of the puzzle.

    Find the total minimum button presses for all machines (joltage mode).

    Args:
        data: The puzzle input

    Returns:
        Total minimum button presses
    """
    total = 0

    for line in data.strip().split("\n"):
        target, buttons = parse_machine_part2(line)
        presses = solve_machine_part2(target, buttons)
        total += presses

    return total


def run() -> None:
    """Run the day 10 solutions."""
    print("Day 10: Factory")

    data = get_input(10)

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    run()
