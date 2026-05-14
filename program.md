# AutoResearch — Snake AI Optimization

> Autonomous optimization of a Snake game AI to maximize average food eaten.

## Overview

You are an autonomous optimization agent. Your job is to improve a Snake AI
by iteratively modifying `target.py`, evaluating performance across 10 games,
and keeping only improvements. You work indefinitely without human supervision.

## Domain Configuration

- **Domain**: Snake game AI (pathfinding + strategy)
- **Target file**: `target.py`
- **Eval command**: `python evaluate.py`
- **Metric name**: `score`
- **Metric direction**: **higher** is better (average food eaten per game)
- **Time budget per run**: 2 minutes (wall clock)
- **Timeout**: 4 minutes → kill and treat as failure
- **Board**: 20×20 grid, 10 games with seeds 100-109

## Game Rules (what your AI faces)

- Snake starts at center, length 3, moving right
- Food appears at random positions (deterministic per seed)
- Hitting walls = death
- Hitting own body = death
- Each food eaten = +1 score, snake grows by 1
- Max 200 steps without food = stuck (game ends)
- Max total steps = width × height × 10

## The AI Interface

Your `decide(state)` function receives:
```python
state = {
    "head": Point(x, y),        # snake head position
    "snake": [Point, ...],      # all body segments (head first)
    "food": Point(x, y),        # current food position
    "direction": Direction,      # current movement direction
    "width": 20,                # board width
    "height": 20,               # board height
    "score": int,               # food eaten so far
    "steps": int,               # total steps taken
}
```

Must return: `Direction.UP`, `Direction.DOWN`, `Direction.LEFT`, or `Direction.RIGHT`

## What You CAN Do

- Implement any pathfinding algorithm (BFS, A*, greedy)
- Use heuristics (Manhattan distance, wall avoidance)
- Implement look-ahead / simulation
- Use Hamilton cycle or spanning tree approaches
- Combine strategies (e.g., greedy early, cautious when long)
- Import only from: `snake_engine`, `random`, `collections`, `heapq`, `math`

## What You CANNOT Do

- Modify `evaluate.py`, `snake_engine.py`, or `program.md`
- Use external packages (no numpy, no scipy)
- Use threading or multiprocessing
- Hard-code moves for specific seeds
- Change the function signature: `def decide(state: dict) -> Direction`
- Access the game's RNG or future food positions

## Strategy Ideas (progression path)

1. **Greedy chase** — always move toward food (avoids walls) → ~5-10 score
2. **BFS shortest path** — find shortest safe path to food → ~15-25 score
3. **A* with body avoidance** — pathfind around own body → ~25-40 score
4. **Look-ahead** — check if a move leaves an escape path → ~40-60 score
5. **Hamilton cycle** — follow a space-filling path → ~80-150 score (safe but slow)
6. **Shortcutting Hamilton** — take shortcuts when safe → ~150-300 score
7. **Hybrid** — greedy when short, Hamilton when long → maximum score

## Simplicity Criterion

> All else being equal, simpler is better.
> A simple BFS that scores 30 beats a complex mess that scores 31.
> But a Hamilton cycle that scores 150 beats a simple greedy at 10.

## The Experiment Loop

LOOP FOREVER:
1. Read `target.py` and recent entries in `results.tsv`
2. Analyze what strategies have been tried and their scores
3. Form a hypothesis for improvement
4. Modify `target.py`
5. `git add -A && git commit -m "experiment: <brief description>"`
6. Run: `python evaluate.py`
7. Extract metric from stdout: the line starting with `score:`
8. Compare against best score in `results.tsv`
9. If improved → log as `keep` in `results.tsv`
10. If NOT improved → log as `discard`, then `git reset --hard HEAD~1`
11. If crashed → attempt fix, otherwise log as `crash` and revert
12. Go to step 1

## Logging

Append to `results.tsv` (TAB-separated):
```
commit	score	status	description
```

## NEVER STOP

Continue working INDEFINITELY. If you've reached a good score,
push further. There is always room for improvement. Try hybrid
approaches, edge-case handling, efficiency tweaks.
