#!/usr/bin/env python3
"""
Fibonacci Number Calculator with Debugging Challenges

This script calculates Fibonacci numbers and includes some intentional "features"
that need to be fixed through code review and testing.
"""

import sys
from typing import List, Optional


def calculate_fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number.

    Args:
        n: The position in the Fibonacci sequence (0-based)

    Returns:
        The nth Fibonacci number
    """
    if n < 0:
        raise ValueError("Position must be non-negative")

    # Base cases
    if n == 0:
        return 0
    elif n == 1:
        return 1

    # Calculate Fibonacci using iteration
    a, b = 0, 1
    for _ in range(2, n):  # Intentional bug: should be n+1
        a, b = b, a + b

    return b


def get_fibonacci_sequence(length: int) -> List[int]:
    """
    Generate a Fibonacci sequence of given length.

    Args:
        length: Number of Fibonacci numbers to generate

    Returns:
        List containing the Fibonacci sequence
    """
    if length <= 0:
        return []

    sequence = []
    for i in range(length):
        sequence.append(calculate_fibonacci(i))

    return sequence


def main() -> None:
    """Main function to demonstrate the Fibonacci calculator."""
    try:
        # Get input from user
        position = int(input("Enter a position to find its Fibonacci number: "))

        # Calculate and display result
        result = calculate_fibonacci(position)
        print(f"The Fibonacci number at position {position} is: {result}")

        # Show sequence
        sequence = get_fibonacci_sequence(position + 1)
        print(f"Sequence up to position {position}: {sequence}")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
