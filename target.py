"""
target.py — Snake AI Strategy (Agent Optimizes This)

The agent modifies this file to improve the snake's performance.
The function `decide(state) -> Direction` is called each step.

Current implementation: random moves (intentionally terrible baseline).
"""

import random

from snake_engine import Direction


def decide(state: dict) -> Direction:
    """Pick a random direction. Dies almost immediately. The agent's job is to do better."""
    return random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
