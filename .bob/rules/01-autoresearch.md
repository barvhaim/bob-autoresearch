# Bob AutoResearch — Loop Rules (Snake AI)

You are optimizing a **Snake game AI** inside an AutoResearch loop.

## Critical Rules

1. **Read `program.md` first** — it has all instructions and strategy ideas
2. **ONE iteration per invocation** — one change, evaluate, commit or revert
3. **Never modify `evaluate.py` or `snake_engine.py`** — they are immutable
4. **Never modify `program.md`** — it is immutable
5. **Always log to `results.tsv`** — TAB-separated, append only
6. **Commit before evaluating** — so you can revert cleanly
7. **Revert failed experiments** — `git reset --hard HEAD~1`
8. **Read `results.tsv` first** — learn from past experiments, don't repeat failures

## Strategy Progression

Start simple, build up:
- Random → Greedy → BFS → A* → Hamilton → Hybrid

Don't jump to the most complex approach first. Each iteration should be
an incremental improvement over the current code.

## Import Rules

Only use: `snake_engine`, `random`, `collections`, `heapq`, `math`
No external packages!
