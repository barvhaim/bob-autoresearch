# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A demo of **autonomous code optimization**: an outer loop (`run.sh`) repeatedly invokes the `bob` CLI agent, which edits a single Snake-AI strategy file (`target.py`), runs an evaluator, and either keeps the change (if the score improved) or reverts it via `git reset --hard HEAD~1`. It is an adaptation of Karpathy's AutoResearch pattern.

The project's primary "user" is **the agent inside the loop**, not a human writing features. Most code changes that humans make here are to the harness (eval, engine, replay, prompt), not to the strategy itself.

## Commands

```bash
# Evaluate the current target.py (10 seeded games, prints "score: X.XX")
python evaluate.py
python evaluate.py --replay        # plus an ASCII replay of the best game

# Watch the AI play one game (ASCII animation)
python replay.py                    # default seed 100
python replay.py --seed 105 --slow

# Visual replay (separate, larger renderer — see visual_replay.py)
python visual_replay.py --seed 100

# Run the autonomous optimization loop (requires BOBSHELL_API_KEY)
./run.sh                            # unlimited
./run.sh --max-iterations 10        # bounded — what the demo uses
./run.sh --dry-run                  # show the bob command without running
```

There is no test suite, linter, or build step. `python evaluate.py` IS the test — its `score:` line is the only metric that matters.

## Files and who is allowed to touch them

This contract is load-bearing for the demo. Violating it breaks the loop's invariants.

| File | Role | Modifiable by |
|------|------|---------------|
| `target.py` | Snake AI strategy (the thing being optimized) | **Bob agent only** — humans reset it to the random baseline before demos |
| `evaluate.py`, `snake_engine.py` | Harness — game rules and scoring | **Nobody during a run.** Treat as immutable. |
| `program.md` | The English-language spec Bob reads each iteration | Human only, rarely |
| `.bob/rules/*.md` | Bob's project rules (loaded by the `bob` CLI) | Human only |
| `results.tsv` | Append-only experiment ledger (TAB-separated: `commit  score  status  description`) | Bob (append) |
| `run.sh` | Outer loop wrapper around the `bob` CLI | Human only |
| `replay.py`, `visual_replay.py` | Demo visualization | Human only |

If you (Claude) are asked to "improve the snake AI," you are stepping into Bob's role — modify only `target.py` and follow the loop discipline in `program.md` (commit, evaluate, keep-or-revert, log to `results.tsv`).

If you are asked to change the harness, evaluator, or prompt, stay out of `target.py`.

## The ratchet loop (architecture)

```
run.sh
  └── bob -y "<BOB_PROMPT>" [repeat]
        ├── reads program.md, target.py, results.tsv
        ├── edits target.py
        ├── git commit
        ├── python evaluate.py
        ├── parses "score:" line from stdout
        ├── if score > best in results.tsv  → append "keep" row
        └── else                            → append "discard" row + git reset --hard HEAD~1
```

Two consequences worth remembering:

- **Every commit on this branch is supposed to be a validated improvement.** `git log --oneline` is itself the demo artifact. Don't make non-improvement commits to this branch during a run.
- **`results.tsv` is the agent's memory across iterations.** The `BOB_PROMPT` in `run.sh` instructs Bob to read it before each attempt to avoid repeating failed strategies. Don't rewrite history in this file.

## Evaluation contract (don't break these)

`evaluate.py` and `snake_engine.py` define the contract `target.py` must satisfy. If you change either, the agent's prior results become incomparable.

- `target.py` exposes `decide(state: dict) -> Direction`. State keys are listed in `program.md`. Returning a non-`Direction` ends that game with the score so far.
- 10 games, board 20×20, seeds 100–109. Score = mean food eaten across the 10 games.
- Stuck detection: 200 steps without eating ends the game.
- Allowed imports inside `target.py`: `snake_engine`, `random`, `collections`, `heapq`, `math`. No numpy, no threading, no multiprocessing. (Enforced socially via `program.md`, not technically.)
- The evaluator prints multiple metrics but the final `score: X.XX` line is what `run.sh` and the agent parse. Don't change that format.

## Resetting for a demo

The demo starts from the random baseline. After a run, restore the baseline before the next one:

```bash
git checkout target.py             # if the random baseline is the committed version
# clear results.tsv to just its header line:
printf "commit\tscore\tstatus\tdescription\n" > results.tsv
git status                         # must be clean before starting
python evaluate.py                 # baseline should be ~0.10
```

`DEMO.md` is the live presentation script — consult it for the intended user-facing flow rather than inferring it from code.

## Requirements

- Python 3.10+ (uses `tuple[bool, int]` builtins generics)
- `bob` CLI (`npm install -g bobshell`) with `BOBSHELL_API_KEY` exported, only needed to run the loop itself — `evaluate.py` and `replay.py` work without it.
