"""
Snake Game Engine — DO NOT MODIFY

A deterministic Snake game engine used by evaluate.py.
The agent does NOT touch this file.
"""

import random
from enum import Enum
from typing import NamedTuple


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Point(NamedTuple):
    x: int
    y: int


class SnakeGame:
    """Deterministic Snake game for AI evaluation."""

    def __init__(self, width: int = 20, height: int = 20, seed: int = 42):
        self.width = width
        self.height = height
        self.rng = random.Random(seed)

        # Snake starts in the center, moving right
        center = Point(width // 2, height // 2)
        self.snake = [center, Point(center.x - 1, center.y), Point(center.x - 2, center.y)]
        self.direction = Direction.RIGHT
        self.food = self._place_food()
        self.score = 0
        self.steps = 0
        self.max_steps = width * height * 10  # prevent infinite loops
        self.game_over = False

    def _place_food(self) -> Point:
        """Place food at a random empty cell."""
        empty = set()
        for x in range(self.width):
            for y in range(self.height):
                p = Point(x, y)
                if p not in self.snake:
                    empty.add(p)
        if not empty:
            return Point(-1, -1)  # board full = win
        return self.rng.choice(list(sorted(empty)))  # sorted for determinism

    def get_state(self) -> dict:
        """Return the current game state (what the AI sees)."""
        head = self.snake[0]
        return {
            "head": head,
            "snake": list(self.snake),
            "food": self.food,
            "direction": self.direction,
            "width": self.width,
            "height": self.height,
            "score": self.score,
            "steps": self.steps,
        }

    def step(self, action: Direction) -> tuple[bool, int]:
        """Execute one step. Returns (alive, score).

        The AI provides a Direction. Invalid 180° turns are ignored
        (keeps current direction).
        """
        if self.game_over:
            return False, self.score

        # Prevent 180° reversal
        opposite = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        if action != opposite.get(self.direction):
            self.direction = action

        # Move head
        dx, dy = self.direction.value
        new_head = Point(self.snake[0].x + dx, self.snake[0].y + dy)

        # Check wall collision
        if not (0 <= new_head.x < self.width and 0 <= new_head.y < self.height):
            self.game_over = True
            return False, self.score

        # Check self collision (excluding tail which will move)
        if new_head in self.snake[:-1]:
            self.game_over = True
            return False, self.score

        self.snake.insert(0, new_head)

        # Check food
        if new_head == self.food:
            self.score += 1
            self.food = self._place_food()
        else:
            self.snake.pop()

        self.steps += 1

        # Timeout check
        if self.steps >= self.max_steps:
            self.game_over = True

        return not self.game_over, self.score

    def render(self) -> str:
        """Render the board as ASCII art."""
        grid = [["." for _ in range(self.width)] for _ in range(self.height)]

        for i, p in enumerate(self.snake):
            if 0 <= p.x < self.width and 0 <= p.y < self.height:
                grid[p.y][p.x] = "O" if i == 0 else "o"

        if 0 <= self.food.x < self.width and 0 <= self.food.y < self.height:
            grid[self.food.y][self.food.x] = "*"

        border = "+" + "-" * self.width + "+"
        lines = [border]
        for row in grid:
            lines.append("|" + "".join(row) + "|")
        lines.append(border)
        lines.append(f"Score: {self.score}  Steps: {self.steps}")
        return "\n".join(lines)
