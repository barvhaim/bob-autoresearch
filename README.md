# Bob AutoResearch — Snake AI Demo 🐍🔄

**Watch Bob Shell autonomously evolve a Snake AI from random moves to intelligent pathfinding.**

An adaptation of [Karpathy's AutoResearch](https://github.com/karpathy/autoresearch) pattern for IBM Bob Shell.

## The Demo

Bob starts with a Snake AI that moves **randomly** (score: ~1 food).
Over 10-15 iterations, it evolves through:

```
Random (~1) → Greedy (~8) → BFS (~20) → A* (~35) → Look-ahead (~50) → Hamilton (~150+)
```

Each iteration takes ~1-2 minutes. You can watch the score climb in real-time.

## Quick Start

```bash
git clone https://github.com/njs2017/bob-autoresearch
cd bob-autoresearch
git checkout demo/snake-ai

# See the terrible baseline
python evaluate.py

# Watch the AI play (random = hilarious)
python replay.py

# Start the optimization loop
./run.sh

# In another terminal — watch the AI improve
python replay.py --seed 100
```

## What Happens During the Demo

```
┌──────────────────────────────────────────────────────┐
│  🔬 Iteration 1  |  14:32:05                        │
│  ═══════════════════════════════════════════════════  │
│  Bob: "Random is terrible. Let me try greedy..."     │
│  📊 Best: 8.40 | Experiments: 1 | Kept: 1           │
├──────────────────────────────────────────────────────┤
│  🔬 Iteration 2  |  14:33:22                        │
│  Bob: "Greedy hits walls. Adding wall avoidance..."  │
│  📊 Best: 12.60 | Experiments: 2 | Kept: 2          │
├──────────────────────────────────────────────────────┤
│  🔬 Iteration 3  |  14:34:45                        │
│  Bob: "Let me try BFS to find shortest path..."      │
│  📊 Best: 22.30 | Experiments: 3 | Kept: 3          │
├──────────────────────────────────────────────────────┤
│  🔬 Iteration 4  |  14:36:01                        │
│  Bob: "BFS doesn't avoid body. Adding A*..."         │
│  📊 Best: 35.10 | Experiments: 4 | Kept: 4          │
└──────────────────────────────────────────────────────┘
```

## Files

| File | Role | Touched by |
|------|------|-----------|
| `program.md` | Instructions for Bob | Human only |
| `target.py` | Snake AI (random baseline) | **Bob only** |
| `evaluate.py` | Runs 10 games, outputs avg score | Nobody |
| `snake_engine.py` | Game logic | Nobody |
| `replay.py` | ASCII visualization for demo | Nobody |
| `run.sh` | Loop wrapper | Nobody |
| `results.tsv` | Experiment log | Bob (append) |

## Demo Tips

1. **Start with `python replay.py`** — show the random AI dying instantly (funny)
2. **Run `./run.sh --max-iterations 10`** — let it run 10 iterations
3. **Between iterations, run `python replay.py`** — show the AI getting smarter
4. **Show `git log --oneline`** — every commit is a validated improvement
5. **Show `results.tsv`** — full experiment history with scores

## Architecture (The Ratchet Loop)

```
run.sh (bash)
  │
  └── bob -y "Do one iteration..." (repeat forever)
        │
        ├── Read program.md + target.py + results.tsv
        ├── Decide on improvement strategy
        ├── Edit target.py
        ├── git commit
        ├── python evaluate.py → score: X.XX
        │
        ├── IF improved → keep commit, log "keep"
        └── IF worse    → git reset --hard HEAD~1, log "discard"
```

## Adapting for Other Domains

See `examples/` for templates:
- `prompt-optimization.md` — LLM prompt tuning
- `web-performance.md` — response time
- `trading-strategy.md` — Sharpe ratio
- `sql-optimization.md` — query speed

The pattern works for anything with: **1 file** + **1 number** + **fast eval**.

## Requirements

- Node.js 18+ (for Bob Shell)
- Python 3.10+
- `bob` CLI installed (`npm install -g bobshell`)
- Git

## License

MIT
