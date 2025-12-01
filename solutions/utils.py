"""Utility functions for Advent of Code 2025."""

import os
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv

BASE_URL = "https://adventofcode.com/2025/day/"


def get_input(day: int) -> str:
    """Fetch the puzzle input for a given day from adventofcode.com.

    Args:
        day: The day number (1-12)

    Returns:
        The puzzle input as a string

    Raises:
        ValueError: If AOC_SESSION environment variable is not set
        requests.HTTPError: If the request fails
    """
    load_dotenv()

    session = os.getenv("AOC_SESSION")
    if not session:
        raise ValueError("AOC_SESSION environment variable not set")

    url = urljoin(BASE_URL, f"{day}/input")
    response = requests.get(url, cookies={"session": session}, timeout=10)
    response.raise_for_status()

    return response.text.strip()
