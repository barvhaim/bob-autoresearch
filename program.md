# AutoResearch — Sorting Algorithm Optimization

> Autonomous optimization of sorting algorithms to minimize execution time.

## Overview

You are an autonomous optimization agent running inside Bob Shell.
Your job is to improve a single metric (sort execution time) by iteratively
modifying `target.py`, evaluating results, and keeping only improvements.

## Domain Configuration

- **Domain**: Sorting algorithm optimization
- **Target file**: `target.py`
- **Eval command**: `python evaluate.py`
- **Metric name**: `score`
- **Metric direction**: **lower** is better (seconds)
- **Time budget per run**: 2 minutes (wall clock)
- **Timeout**: 4 minutes → kill and treat as failure

## What You CAN Do

- Replace the sorting algorithm entirely
- Optimize inner loops, data structures, memory usage
- Use Python built-ins (`sorted()`, `list.sort()`)
- Use standard library modules (`heapq`, `bisect`, `array`)
- Add type hints or micro-optimizations
- Delete unnecessary code (simplification wins!)

## What You CANNOT Do

- Modify `evaluate.py`
- Modify this file (`program.md`)
- Install external packages (no numpy, no C extensions)
- Modify the function signature: `def sort_array(arr: list) -> list`
- Use multiprocessing or threading
- Cache or memoize results between evaluation runs
- Read the test data from evaluate.py in advance

## Simplicity Criterion

> All else being equal, simpler is better.
> Tiny improvement + ugly complexity? Probably not worth it.
> Tiny improvement from deleting code? Definitely keep.
> ~0 improvement but much simpler code? Keep.

## The Experiment Loop

LOOP FOREVER:
1. Read `target.py` and the last 20 entries in `results.tsv`
2. Analyze what has been tried and what worked
3. Form a hypothesis for improvement
4. Modify `target.py`
5. `git add -A && git commit -m "experiment: <brief description>"`
6. Run: `python evaluate.py`
7. Extract metric from stdout: the line starting with `score:`
8. Compare against best score in `results.tsv`
9. If improved → log as `keep` in `results.tsv`
10. If NOT improved → log as `discard`, then `git reset --hard HEAD~1`
11. If crashed → attempt trivial fix, otherwise log as `crash` and revert
12. Go to step 1

## Logging

Append to `results.tsv` (TAB-separated, NOT commas):
```
commit	score	status	description
```

- `commit`: short git hash (first 7 chars)
- `score`: the metric value (float, seconds)
- `status`: one of `keep`, `discard`, `crash`
- `description`: one-line summary of what was tried

## NEVER STOP

Once the experiment loop has begun, do NOT pause to ask the human
if you should continue. Continue working INDEFINITELY until manually stopped.
If you run out of ideas, think harder. There is always something to try:
- Different algorithm families (merge, quick, radix, tim, intro)
- Hybrid approaches (switch algorithm based on input size)
- Memory layout optimizations
- Python-specific tricks (list comprehensions, `__slots__`, etc.)
