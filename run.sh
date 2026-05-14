#!/usr/bin/env bash
#
# run.sh — AutoResearch Loop Runner for Bob Shell
#
# Wraps Bob in an infinite loop. Each iteration:
#   1. Bob reads program.md
#   2. Makes ONE change to target.py
#   3. Evaluates, commits or reverts
#   4. Logs to results.tsv
#
# Usage:
#   ./run.sh                    # default: unlimited iterations
#   ./run.sh --max-iterations 50
#   ./run.sh --max-coins 30     # per-iteration coin cap
#   ./run.sh --dry-run          # show what would run
#
# Stop: Ctrl+C (graceful — current iteration finishes)
#

set -euo pipefail

# ─── Configuration ───────────────────────────────────────────────
MAX_ITERATIONS=0          # 0 = unlimited
MAX_COINS=50              # per-iteration Bob coin cap
CHAT_MODE="code"          # code or advanced
SLEEP_BETWEEN=3           # seconds between iterations
BOB_FLAGS=""              # extra flags passed to bob
DRY_RUN=false

# ─── Parse CLI args ─────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --max-iterations) MAX_ITERATIONS="$2"; shift 2 ;;
    --max-coins)      MAX_COINS="$2"; shift 2 ;;
    --chat-mode)      CHAT_MODE="$2"; shift 2 ;;
    --sleep)          SLEEP_BETWEEN="$2"; shift 2 ;;
    --dry-run)        DRY_RUN=true; shift ;;
    --bob-flags)      BOB_FLAGS="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# ─── Prompt for Bob (each iteration) ────────────────────────────
BOB_PROMPT='Read program.md carefully. Review the current target.py and the last 20 entries in results.tsv.

You are doing ONE iteration of the AutoResearch optimization loop:
1. Analyze what has been tried (results.tsv) and the current code (target.py)
2. Form a hypothesis for improvement
3. Modify target.py
4. Run: git add -A && git commit -m "experiment: <brief description>"
5. Run: python evaluate.py
6. Extract the score from output (line starting with "score:")
7. Compare against the best score in results.tsv
8. If improved: append a "keep" line to results.tsv
9. If NOT improved: append a "discard" line, then run: git reset --hard HEAD~1
10. If crashed: attempt fix, otherwise append "crash" line and revert

Format for results.tsv (TAB-separated):
commit<TAB>score<TAB>status<TAB>description

Where commit = short git hash, score = float, status = keep/discard/crash.

Do exactly ONE iteration. Do not ask questions. Do not stop to confirm.'

# ─── State ───────────────────────────────────────────────────────
ITERATION=0
STARTTIME=$(date +%s)

# ─── Trap Ctrl+C ────────────────────────────────────────────────
trap 'echo -e "\n🛑 Stopped after $ITERATION iterations."; exit 0' INT TERM

# ─── Banner ──────────────────────────────────────────────────────
echo "╔═══════════════════════════════════════════════════════╗"
echo "║         🔄 Bob AutoResearch Loop Runner              ║"
echo "╠═══════════════════════════════════════════════════════╣"
echo "║  Max iterations : $(printf '%-10s' "${MAX_ITERATIONS:-∞}")                        ║"
echo "║  Max coins/iter : $(printf '%-10s' "$MAX_COINS")                        ║"
echo "║  Chat mode      : $(printf '%-10s' "$CHAT_MODE")                        ║"
echo "║  Sleep between  : $(printf '%-10s' "${SLEEP_BETWEEN}s")                        ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

if $DRY_RUN; then
  echo "🏜️  DRY RUN — would execute:"
  echo "  bob -y --chat-mode=$CHAT_MODE --max-coins $MAX_COINS $BOB_FLAGS \"<prompt>\""
  exit 0
fi

# ─── Main Loop ───────────────────────────────────────────────────
while true; do
  ITERATION=$((ITERATION + 1))

  # Check iteration limit
  if [[ $MAX_ITERATIONS -gt 0 && $ITERATION -gt $MAX_ITERATIONS ]]; then
    echo "✅ Reached max iterations ($MAX_ITERATIONS). Stopping."
    break
  fi

  # Header
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  🔬 Iteration $ITERATION  |  $(date '+%Y-%m-%d %H:%M:%S')"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Run Bob
  bob -y \
    --chat-mode="$CHAT_MODE" \
    --max-coins "$MAX_COINS" \
    --hide-intermediary-output \
    $BOB_FLAGS \
    "$BOB_PROMPT" \
    2>&1 || {
      echo "⚠️  Bob exited with error (code $?). Continuing..."
    }

  # Show current best
  if [[ -f results.tsv ]] && [[ $(wc -l < results.tsv) -gt 1 ]]; then
    BEST=$(grep "keep" results.tsv | sort -t$'\t' -k2 -n | head -1 | cut -f2)
    LAST=$(tail -1 results.tsv)
    echo ""
    echo "  📊 Best score so far: ${BEST:-N/A}"
    echo "  📝 Last result: $LAST"
  fi

  # Sleep
  echo "  ⏳ Sleeping ${SLEEP_BETWEEN}s..."
  sleep "$SLEEP_BETWEEN"
done

# ─── Summary ─────────────────────────────────────────────────────
ENDTIME=$(date +%s)
ELAPSED=$(( ENDTIME - STARTTIME ))
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  🏁 AutoResearch Complete"
echo "  Iterations: $ITERATION"
echo "  Duration: $((ELAPSED / 3600))h $((ELAPSED % 3600 / 60))m $((ELAPSED % 60))s"
if [[ -f results.tsv ]]; then
  KEEPS=$(grep -c "keep" results.tsv 2>/dev/null || echo 0)
  DISCARDS=$(grep -c "discard" results.tsv 2>/dev/null || echo 0)
  echo "  Kept: $KEEPS  Discarded: $DISCARDS"
fi
echo "═══════════════════════════════════════════════════════════"
