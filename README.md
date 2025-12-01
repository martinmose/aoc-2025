# Advent of Code 2025

My solutions for [Advent of Code 2025](https://adventofcode.com/2025) in Python.

This year features 12 days of puzzles instead of the usual 25.

## Setup

1. Install [Flox](https://flox.dev) and activate the environment:

```bash
flox activate
```

This automatically:
- Sets up the right Python version 
- Creates a virtual environment
- Installs all dependencies

2. Create a `.env` file with your AoC session cookie:

```bash
AOC_SESSION=your_session_cookie_here
```

To get your session cookie:
- Log in to [adventofcode.com](https://adventofcode.com)
- Open browser dev tools (F12)
- Go to Application/Storage > Cookies
- Copy the value of the `session` cookie

## Running Solutions

Run all solutions:
```bash
python main.py
```

Run a specific day:
```bash
python -m solutions.day1.day1
```

## Testing

```bash
pytest
```

## Code Quality

```bash
lint      # ruff check + mypy
fmt       # ruff format
check     # lint + format check + tests
```

Or run individually:
```bash
ruff check .      # Linting
ruff format .     # Formatting
mypy .            # Type checking
```
