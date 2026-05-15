# Demo Cheat-Sheet — Bob AutoResearch (Snake)

**Total time:** ~10 minutes. **Setup:** two terminals side-by-side. Left = loop. Right = commentary.

---

## Pre-flight (do once, before audience arrives)

```bash
python evaluate.py     # confirm baseline ~0.10
git status             # must be clean
git log --oneline      # tidy starting point
```

If baseline is not ~0.10, the random reset got lost — re-apply `target.py` and clear `results.tsv` to header.

---

## Act 1 — "Look how bad it starts" (90s)

**Right terminal:**

```bash
cat target.py                        # ~3 lines of random.choice
python visual_replay.py --seed 100   # snake dies in seconds — get the laugh
python evaluate.py                   # score: 0.10
```

**Say:** *"This is the starting point. Bob hasn't touched it yet."*

---

## Act 2 — Hand the keys to Bob

**Left terminal:**

```bash
./run.sh --max-iterations 10
```

**Narrate while it runs:** *"Bob reads `program.md`, edits `target.py`, commits, evaluates, keeps or reverts. Repeat."*

---

## Act 3 — Watch the score climb (5–7 min)

After iterations **1, 3, 5, 8** — run this trio in the right terminal:

```bash
git log --oneline                    # every commit is a validated improvement
cat results.tsv                      # ledger — note the `discard` rows
python visual_replay.py --seed 100   # SAME seed every time — direct comparison
```

**Always replay seed 100.** Same food sequence, visibly smarter snake. That's the punch.

---

## Act 4 — Land the point (60s)

```bash
cat program.md | head -40            # the only thing the human wrote
git log --oneline | head -15         # what Bob produced
```

**Say:** *"I didn't write any of this Python. I wrote `program.md` — the instructions — and Bob did the research. Humans program agents; agents program code."*

---

## Cue cards — moments to call out

| When you see this | Say this |
|---|---|
| First successful `keep` | *"That's iteration 1 — already 10x better than random."* |
| A `discard` in results.tsv | *"Bob just threw away a worse experiment. The ratchet only goes up."* |
| A crash + revert | *"Failures are the demo. The loop catches bad ideas without me."* |
| Score crosses ~30 | *"For comparison, my hand-written greedy AI scored 36. Bob got here in N minutes."* |
| Score crosses ~80 | *"This is Hamilton-cycle territory. Bob figured that out from one English-language spec."* |

---

## If things go sideways

- **Bob hangs / network slow** → switch to backup recording (record beforehand with `asciinema rec demo.cast`).
- **An iteration crashes** → don't apologize, point at it: *"This is the loop catching a bad idea. Watch — `git reset` reverts it."*
- **Score plateaus early** → skip ahead: `Ctrl+C` the loop, run `python visual_replay.py --seed 100` and pivot to Act 4.
- **Audience asks "how does Bob decide what to try?"** → open `program.md`, point at the "Strategy Ideas" section.

---

## Don't

- Don't run `--max-iterations 30` live — gains slow after ~6 and the audience drifts.
- Don't read the Python Bob writes — story is "score climbed," not "look at this BFS."
- Don't show `snake_engine.py` or `evaluate.py` unless asked — that's infrastructure, not the demo.
- Don't change seeds between replays — it kills the visual comparison.

---

## One-line elevator version

> *Random snake. Bob reads English. 10 minutes later, the snake plays like a human.*
