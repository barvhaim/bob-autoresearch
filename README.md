# Bob AutoResearch 🔄🤖

**Karpathy's AutoResearch pattern, adapted for IBM Bob Shell.**

An autonomous optimization loop where Bob Shell iteratively improves code
against a scalar metric — keeping only improvements via git rollback.

## What is AutoResearch?

An open-ended optimization loop (originated by [Andrej Karpathy](https://github.com/karpathy/autoresearch)):

```
┌─────────────────────────────────────────┐
│          Read program.md                │
│               ↓                         │
│    ┌── Read target.py + results.tsv     │
│    │         ↓                          │
│    │   Form hypothesis                  │
│    │         ↓                          │
│    │   Modify target.py                 │
│    │         ↓                          │
│    │   git commit                       │
│    │         ↓                          │
│    │   Run evaluate.py                  │
│    │         ↓                          │
│    │   ┌─ Improved? ─┐                  │
│    │   │ YES         │ NO               │
│    │   │ Keep ✓      │ git reset ✗      │
│    │   └─────────────┘                  │
│    │         ↓                          │
│    │   Log to results.tsv               │
│    │         ↓                          │
│    └──── LOOP FOREVER ◄─────────────────│
└─────────────────────────────────────────┘
```

## Three-File Architecture

| File | Role | Who Touches It |
|------|------|---------------|
| `program.md` | Instructions for Bob | **Human only** |
| `target.py` | Code being optimized | **Bob only** |
| `evaluate.py` | Immutable scorer | **Nobody** (sacred) |

Supporting: `results.tsv` (auto-generated experiment log)

## Quick Start

```bash
# 1. Clone this repo
git clone <this-repo>
cd bob-autoresearch

# 2. Run the baseline
python evaluate.py
# → score: ~9.8 seconds (bubble sort)

# 3. Launch the loop
./run.sh
# Bob will optimize target.py overnight

# 4. Check progress
tail -f results.tsv
git log --oneline
```

## How It Works with Bob Shell

Since Bob doesn't have a built-in loop mode, we use a **wrapper script** (`run.sh`)
that calls Bob in one-shot mode for each iteration:

```
run.sh (bash loop)
  └── bob -y --chat-mode=code "Do one iteration..."
       └── Bob reads program.md → edits target.py → evaluates → commits/reverts
  └── (repeat forever)
```

This is actually **more robust** than a single long session:
- If Bob crashes → the script restarts it
- Each iteration gets fresh context
- `--max-coins` caps cost per iteration

## Adapting for Your Domain

1. Replace `evaluate.py` with your metric
2. Replace `target.py` with your naive starting code
3. Edit `program.md` — update the Domain Configuration section
4. See `examples/` for templates (prompts, web perf, trading, SQL)

### The 3 Conditions

Your domain must satisfy:
- ✅ **Single file** the agent modifies
- ✅ **Scalar metric** (one number — lower/higher = better)
- ✅ **Fast evaluation** (minutes, not hours)

## Files

```
bob-autoresearch/
├── README.md              ← You are here
├── program.md             ← Agent instructions (sorting optimization example)
├── target.py              ← Bubble sort baseline (agent optimizes this)
├── evaluate.py            ← Immutable evaluator (times sorting on arrays)
├── results.tsv            ← Experiment log (tab-separated)
├── run.sh                 ← Loop wrapper script
├── .bob/
│   └── rules/
│       └── 01-autoresearch.md  ← Bob-specific rules for the loop
├── .gitignore
└── examples/
    ├── prompt-optimization.md
    ├── web-performance.md
    ├── trading-strategy.md
    └── sql-optimization.md
```

## License

MIT
