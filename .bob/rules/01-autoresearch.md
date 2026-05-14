# Bob AutoResearch — Loop Rules

You are running inside an **AutoResearch optimization loop**.

## Critical Rules

1. **Read `program.md` first** — it has all instructions
2. **ONE iteration per invocation** — make one change, evaluate, commit or revert
3. **Never modify `evaluate.py`** — it is immutable
4. **Never modify `program.md`** — it is immutable
5. **Always log to `results.tsv`** — TAB-separated, append only
6. **Always commit before evaluating** — so you can revert cleanly
7. **Revert failed experiments** — `git reset --hard HEAD~1`
8. **Read `results.tsv`** before making changes — learn from past experiments
9. **Prefer simplicity** — delete code for same performance = always a win

## Git Workflow

```bash
# After modifying target.py:
git add -A && git commit -m "experiment: <description>"

# After evaluation:
# If improved → keep (commit stays)
# If not improved → git reset --hard HEAD~1
```

## Common Mistakes to Avoid

- Don't forget to revert on failure
- Don't use external packages not in stdlib
- Don't modify the function signature in target.py
- Don't skip logging to results.tsv
