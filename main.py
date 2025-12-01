"""Advent of Code 2025 - Main entry point."""

from dotenv import load_dotenv

from solutions.day1.day1 import run as day1_run


def main() -> None:
    """Run all Advent of Code 2025 solutions."""
    load_dotenv()

    print("Advent of Code 2025")
    print("=" * 40)

    days = [
        ("Day 1", day1_run),
        # ("Day 2", day2_run),
    ]

    for name, run_fn in days:
        print(f"\nRunning {name}...")
        try:
            run_fn()
            print(f"{name} completed successfully.")
        except Exception as e:
            print(f"Error in {name}: {e}")


if __name__ == "__main__":
    main()
