"""
evaluate.py — Snake AI Evaluator (DO NOT MODIFY)

Runs multiple games with different seeds and computes average score.
The metric is average food eaten (higher = better).

Usage:
    python evaluate.py
    python evaluate.py --replay     # show ASCII replay of best game
    python evaluate.py --gif        # generate GIF of best game (requires pillow)
"""

import sys
import time
from snake_engine import SnakeGame, Direction

# === Evaluation Config ===
NUM_GAMES = 10
BOARD_SIZE = 20
SEEDS = list(range(100, 100 + NUM_GAMES))  # deterministic seeds
MAX_STEPS_PER_FOOD = 200  # max steps without eating before we call it "stuck"


def run_game(seed: int, verbose: bool = False) -> dict:
    """Run one game and return stats."""
    game = SnakeGame(width=BOARD_SIZE, height=BOARD_SIZE, seed=seed)

    try:
        from target import decide
    except ImportError as e:
        return {"score": 0, "steps": 0, "error": str(e)}
    except SyntaxError as e:
        return {"score": 0, "steps": 0, "error": f"SyntaxError: {e}"}

    last_score = 0
    steps_since_food = 0
    frames = []

    while not game.game_over:
        state = game.get_state()

        try:
            action = decide(state)
        except Exception as e:
            if verbose:
                print(f"  AI error: {e}")
            break

        # Validate return type
        if not isinstance(action, Direction):
            if verbose:
                print(f"  AI returned non-Direction: {action}")
            break

        alive, score = game.step(action)

        # Track stuck detection
        if score > last_score:
            steps_since_food = 0
            last_score = score
        else:
            steps_since_food += 1

        if steps_since_food > MAX_STEPS_PER_FOOD:
            if verbose:
                print(f"  Stuck! No food for {MAX_STEPS_PER_FOOD} steps.")
            break

        if verbose:
            frames.append(game.render())

    return {
        "score": game.score,
        "steps": game.steps,
        "error": None,
        "frames": frames if verbose else [],
    }


def main():
    replay_mode = "--replay" in sys.argv
    verbose = replay_mode

    print("=" * 60)
    print("AutoResearch Evaluator — Snake AI Benchmark")
    print(f"Games: {NUM_GAMES} | Board: {BOARD_SIZE}x{BOARD_SIZE} | Seeds: {SEEDS[0]}-{SEEDS[-1]}")
    print("=" * 60)

    results = []
    best_game = None
    best_score = -1

    start_time = time.perf_counter()

    for seed in SEEDS:
        result = run_game(seed, verbose=verbose)
        results.append(result)

        status = "OK" if not result["error"] else f"ERR: {result['error']}"
        print(f"  seed={seed}  score={result['score']:>3}  steps={result['steps']:>5}  {status}")

        if result["score"] > best_score:
            best_score = result["score"]
            best_game = result

    elapsed = time.perf_counter() - start_time

    # Compute metrics
    scores = [r["score"] for r in results]
    avg_score = sum(scores) / len(scores)
    max_score = max(scores)
    min_score = min(scores)
    errors = sum(1 for r in results if r["error"])

    print("=" * 60)
    print(f"  avg_score: {avg_score:.2f}")
    print(f"  max_score: {max_score}")
    print(f"  min_score: {min_score}")
    print(f"  errors: {errors}/{NUM_GAMES}")
    print(f"  time: {elapsed:.2f}s")
    print("=" * 60)

    if errors == NUM_GAMES:
        print("status: FAIL (all games errored)")
        print("score: 0.0")
        sys.exit(1)

    # Final score: average food eaten across all games
    print(f"score: {avg_score:.2f}")
    print("status: OK")

    # Replay best game
    if replay_mode and best_game and best_game.get("frames"):
        print(f"\n🎮 Replay of best game (score={best_score}):")
        print("-" * 40)
        # Show last 5 frames
        frames = best_game["frames"]
        for frame in frames[-5:]:
            print(frame)
            print()


if __name__ == "__main__":
    main()
