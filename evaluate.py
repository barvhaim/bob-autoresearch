"""
evaluate.py — Immutable Evaluator (DO NOT MODIFY)

Measures sorting performance across multiple array sizes.
Outputs a single scalar metric: total time in seconds.

Usage:
    python evaluate.py
"""

import random
import time
import sys

# Fixed seed for reproducibility across all runs
RANDOM_SEED = 42
TEST_SIZES = [100, 1_000, 5_000, 10_000]
REPEATS = 3  # average over N repeats for stability


def generate_test_data(size: int, seed: int) -> list:
    """Generate a reproducible random array."""
    rng = random.Random(seed)
    return [rng.randint(-1_000_000, 1_000_000) for _ in range(size)]


def verify_sorted(original: list, result: list) -> bool:
    """Verify the result is correctly sorted."""
    if len(result) != len(original):
        return False
    if sorted(original) != result:
        return False
    return True


def main():
    # Import the target function
    try:
        from target import sort_array
    except ImportError as e:
        print(f"error: could not import sort_array from target.py: {e}")
        sys.exit(1)
    except SyntaxError as e:
        print(f"error: syntax error in target.py: {e}")
        sys.exit(1)

    total_time = 0.0
    all_correct = True

    print("=" * 60)
    print("AutoResearch Evaluator — Sorting Benchmark")
    print("=" * 60)

    for size in TEST_SIZES:
        times = []
        for repeat in range(REPEATS):
            seed = RANDOM_SEED + repeat
            data = generate_test_data(size, seed)

            start = time.perf_counter()
            result = sort_array(data)
            elapsed = time.perf_counter() - start
            times.append(elapsed)

            # Verify correctness
            if not verify_sorted(data, result):
                print(f"FAIL: sort_array returned incorrect result for size={size}")
                all_correct = False

        avg_time = sum(times) / len(times)
        total_time += avg_time
        print(f"  size={size:>6,}  avg={avg_time:.6f}s  (runs: {[f'{t:.6f}' for t in times]})")

    print("=" * 60)

    if not all_correct:
        print("status: FAIL (incorrect results)")
        print("score: 999999.0")
        sys.exit(1)

    print(f"score: {total_time:.6f}")
    print("status: OK")


if __name__ == "__main__":
    main()
