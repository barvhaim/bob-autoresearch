"""
target.py — Snake AI Strategy (Agent Optimizes This)

The agent modifies this file to improve the snake's performance.
The function `decide(state) -> Direction` is called each step.

Current implementation: Greedy chase toward food with basic safety.
"""

from snake_engine import Direction, Point


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
    head = state["head"]
    food = state["food"]
    snake = state["snake"]
    width = state["width"]
    height = state["height"]
    
    # Calculate direction preferences based on food position
    dx = food.x - head.x
    dy = food.y - head.y
    
    # Prioritize directions that move toward food
    moves = []
    
    if dx > 0:
        moves.append((abs(dx), Direction.RIGHT))
    elif dx < 0:
        moves.append((abs(dx), Direction.LEFT))
    
    if dy > 0:
        moves.append((abs(dy), Direction.DOWN))
    elif dy < 0:
        moves.append((abs(dy), Direction.UP))
    
    # Sort by distance (prioritize larger distance first)
    moves.sort(reverse=True, key=lambda x: x[0])
    
    # Try each move in order of preference
    for _, direction in moves:
        next_pos = get_next_position(head, direction)
        if is_safe(next_pos, snake, width, height):
            return direction
    
    # If no food-directed move is safe, try any safe move
    for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
        next_pos = get_next_position(head, direction)
        if is_safe(next_pos, snake, width, height):
            return direction
    
    # No safe move found, return any direction (will likely die)
    return Direction.UP


def get_next_position(pos: Point, direction: Direction) -> Point:
    """Calculate the next position given current position and direction."""
    if direction == Direction.UP:
        return Point(pos.x, pos.y - 1)
    elif direction == Direction.DOWN:
        return Point(pos.x, pos.y + 1)
    elif direction == Direction.LEFT:
        return Point(pos.x - 1, pos.y)
    elif direction == Direction.RIGHT:
        return Point(pos.x + 1, pos.y)
    return pos


def is_safe(pos: Point, snake: list, width: int, height: int) -> bool:
    """Check if a position is safe (not wall, not body)."""
    # Check walls
    if pos.x < 0 or pos.x >= width or pos.y < 0 or pos.y >= height:
        return False
    
    # Check body collision (exclude tail since it will move)
    if pos in snake[:-1]:
        return False
    
    return True