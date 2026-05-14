"""
target.py — Snake AI Strategy (Agent Optimizes This)

The agent modifies this file to improve the snake's performance.
The function `decide(state) -> Direction` is called each step.

Current implementation: Random walk (intentionally terrible baseline).
"""

import random
from snake_engine import Direction, Point


# Initialize with a fixed seed for reproducibility within a game
_rng = random.Random(123)


def decide(state: dict) -> Direction:
    """Decide the next move for the snake.

    Args:
        state: dict with keys:
            - head: Point(x, y) — snake's head position
            - snake: list[Point] — all body segments (head first)
            - food: Point(x, y) — current food position
            - direction: Direction — current movement direction
            - width: int — board width
            - height: int — board height
            - score: int — current score
            - steps: int — steps taken so far

    Returns:
        Direction — one of Direction.UP, DOWN, LEFT, RIGHT
    """
    # === TERRIBLE BASELINE: Random direction ===
    # The agent should replace this with something smart.
    return _rng.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
