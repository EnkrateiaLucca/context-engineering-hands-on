"""
lucas.py

A small utility module for working with the Lucas number sequence.

The Lucas sequence is defined similarly to the Fibonacci sequence:
    L(0) = 2
    L(1) = 1
    L(n) = L(n-1) + L(n-2) for n > 1
"""

from functools import lru_cache
from typing import Iterator, List


@lru_cache(maxsize=None)
def lucas(n: int) -> int:
    """Return the nth Lucas number (0-indexed).

    Raises:
        ValueError: if n is negative.
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n == 0:
        return 2
    if n == 1:
        return 1
    return lucas(n - 1) + lucas(n - 2)


def lucas_sequence(count: int) -> List[int]:
    """Return a list containing the first `count` Lucas numbers."""
    if count < 0:
        raise ValueError("count must be a non-negative integer")
    return [lucas(i) for i in range(count)]


def lucas_generator() -> Iterator[int]:
    """Yield an infinite stream of Lucas numbers."""
    a, b = 2, 1
    while True:
        yield a
        a, b = b, a + b


def main() -> None:
    n = 10
    print(f"First {n} Lucas numbers: {lucas_sequence(n)}")

    print(f"L(15) = {lucas(15)}")

    print("Using the generator:")
    gen = lucas_generator()
    print([next(gen) for _ in range(n)])


if __name__ == "__main__":
    main()
