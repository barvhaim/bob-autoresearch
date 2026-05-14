"""
replay.py — Watch the Snake AI play (for demo purposes)

Shows an ASCII animation of the current AI playing a game.
Run this between iterations to show the audience how the AI improved.

Usage:
    python replay.py              # play game with seed 100
    python replay.py --seed 105   # specific seed
    python replay.py --slow       # slower animation (0.2s per frame)
    python replay.py --fast       # faster animation (0.02s per frame)
"""

import sys
import time
import os
from snake_engine import SnakeGame, Direction


def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")


def main():
    seed = 100
    delay = 0.08  # seconds per frame

    # Parse args
    args = sys.argv[1:]
    if "--seed" in args:
        idx = args.index("--seed")
        seed = int(args[idx + 1])
    if "--slow" in args:
        delay = 0.2
    if "--fast" in args:
        delay = 0.02

    # Import AI
    try:
        from target import decide
    except Exception as e:
        print(f"Error importing target.py: {e}")
        sys.exit(1)

    game = SnakeGame(width=20, height=20, seed=seed)
    max_no_food = 200
    steps_since_food = 0
    last_score = 0

    print(f"\n🐍 Snake AI Replay | Seed: {seed} | Delay: {delay}s")
    print("   Press Ctrl+C to stop\n")
    time.sleep(1)

    try:
        while not game.game_over:
            state = game.get_state()

            try:
                action = decide(state)
            except Exception as e:
                print(f"\n❌ AI crashed: {e}")
                break

            if not isinstance(action, Direction):
                print(f"\n❌ AI returned invalid type: {type(action)}")
                break

            alive, score = game.step(action)

            # Stuck detection
            if score > last_score:
                steps_since_food = 0
                last_score = score
            else:
                steps_since_food += 1

            if steps_since_food > max_no_food:
                print(f"\n⏸️  Stuck! No food for {max_no_food} steps.")
                break

            # Render
            clear_screen()
            print(game.render())
            print(f"\n  🎯 Food: {game.food}  |  🐍 Length: {len(game.snake)}")
            time.sleep(delay)

    except KeyboardInterrupt:
        pass

    # Final state
    print("\n" + "=" * 40)
    print(f"  🏁 Game Over!")
    print(f"  Score: {game.score} food eaten")
    print(f"  Steps: {game.steps}")
    print(f"  Length: {len(game.snake)}")
    print("=" * 40)


if __name__ == "__main__":
    main()
