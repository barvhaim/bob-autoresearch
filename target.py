"""
target.py — Sorting Algorithm (Agent Optimizes This)

The agent modifies this file to improve sorting performance.
DO NOT modify evaluate.py or program.md.

Current implementation: Bubble Sort (intentionally naive baseline).
"""


def sort_array(arr: list) -> list:
    """Sort an array of integers in ascending order.

    Args:
        arr: List of integers to sort.

    Returns:
        A new sorted list.
    """
    # Bubble Sort — O(n²) baseline. The agent should replace this.
    result = arr.copy()
    n = len(result)
    for i in range(n):
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
    return result
