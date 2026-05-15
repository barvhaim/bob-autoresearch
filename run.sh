#!/usr/bin/env bash
#
# run.sh — AutoResearch Loop Runner for Bob Shell (Snake AI Demo)
#
# Each iteration Bob improves the Snake AI strategy.
# Watch the score climb from ~1 (random) to 100+ (smart pathfinding).
#
# Usage:
#   ./run.sh                    # unlimited iterations
#   ./run.sh --max-iterations 20
#   ./run.sh --max-coins 30
#
# Stop: Ctrl+C
#

set -euo pipefail

# ─── API Key Check ───────────────────────────────────────────────
if [[ -z "${BOBSHELL_API_KEY:-}" ]]; then
  echo "❌ BOBSHELL_API_KEY not set."
  echo "   export BOBSHELL_API_KEY=<your-key>"
  echo "   Or set it in ~/.bob/settings.json"
  exit 1
fi

# ─── Configuration ───────────────────────────────────────────────
MAX_ITERATIONS=0          # 0 = unlimited
MAX_COINS=50              # per-iteration Bob coin cap
CHAT_MODE="code"
SLEEP_BETWEEN=3
BOB_FLAGS=""
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

# ─── Prompt for Bob ─────────────────────────────────────────────
BOB_PROMPT='Read program.md carefully. Then read target.py and results.tsv.

You are doing ONE iteration of the AutoResearch Snake AI optimization loop:
1. Look at results.tsv — what strategies have been tried? What scored best?
2. Look at target.py — what is the current implementation?
3. Think of a better strategy (see program.md for progression ideas)
4. Modify target.py with your improvement
5. Run: git add -A && git commit -m "experiment: <brief description>"
6. Run: python evaluate.py
7. Look at the "score:" line in the output
8. If score improved vs best in results.tsv: append a TAB-separated "keep" line to results.tsv
9. If NOT improved: append "discard" line, then run: git reset --hard HEAD~1
10. If crashed: try to fix, otherwise append "crash" line and revert

Results.tsv format (TAB-separated): commit<TAB>score<TAB>status<TAB>description

ONE iteration only. No questions. No confirmations.'

# ─── Trap ────────────────────────────────────────────────────────
trap 'echo -e "\n🛑 Stopped after $ITERATION iterations."; exit 0' INT TERM

# ─── Banner ──────────────────────────────────────────────────────
echo ""
echo "  🐍 Bob AutoResearch — Snake AI Optimization"
echo "  ─────────────────────────────────────────────"
echo "  Max iterations : ${MAX_ITERATIONS:-∞}"
echo "  Max coins/iter : $MAX_COINS"
echo "  Chat mode      : $CHAT_MODE"
echo ""

if $DRY_RUN; then
  echo "🏜️  DRY RUN — would execute:"
  echo "  bob -y --auth-method api-key --chat-mode=$CHAT_MODE --max-coins $MAX_COINS $BOB_FLAGS \"<prompt>\""
  exit 0
fi

# ─── Run baseline if first time ─────────────────────────────────
if [[ $(wc -l < results.tsv) -le 1 ]]; then
  echo "  📊 Running baseline evaluation..."
  python evaluate.py 2>&1 | tail -5
  echo ""
fi

# ─── Main Loop ───────────────────────────────────────────────────
ITERATION=0
STARTTIME=$(date +%s)

while true; do
  ITERATION=$((ITERATION + 1))

  if [[ $MAX_ITERATIONS -gt 0 && $ITERATION -gt $MAX_ITERATIONS ]]; then
    echo "✅ Reached max iterations ($MAX_ITERATIONS)."
    break
  fi

  echo ""
  echo "  ═══════════════════════════════════════════════════"
  echo "  🔬 Iteration $ITERATION  |  $(date '+%H:%M:%S')"
  echo "  ═══════════════════════════════════════════════════"

  bob -y \
    --auth-method api-key \
    --chat-mode="$CHAT_MODE" \
    --max-coins "$MAX_COINS" \
    --hide-intermediary-output \
    $BOB_FLAGS \
    "$BOB_PROMPT" \
    2>&1 || {
      echo "  ⚠️  Bob exited with error. Continuing..."
    }

  # Show progress
  if [[ -f results.tsv ]] && [[ $(wc -l < results.tsv) -gt 1 ]]; then
    echo ""
    BEST=$(grep "keep" results.tsv 2>/dev/null | sort -t$'\t' -k2 -rn | head -1 | cut -f2)
    TOTAL=$(tail -n +2 results.tsv | wc -l)
    KEEPS=$(grep -c "keep" results.tsv 2>/dev/null || echo 0)
    echo "  📊 Best: ${BEST:-N/A} | Experiments: $TOTAL | Kept: $KEEPS"
    echo "  📝 Last: $(tail -1 results.tsv)"
  fi

  sleep "$SLEEP_BETWEEN"
done

# ─── Summary ─────────────────────────────────────────────────────
ENDTIME=$(date +%s)
ELAPSED=$(( ENDTIME - STARTTIME ))
echo ""
echo "  ═══════════════════════════════════════════════════"
echo "  🏁 Done! $ITERATION iterations in $((ELAPSED/60))m $((ELAPSED%60))s"
if [[ -f results.tsv ]]; then
  BEST=$(grep "keep" results.tsv 2>/dev/null | sort -t$'\t' -k2 -rn | head -1)
  echo "  🏆 Best result: $BEST"
fi
echo "  ═══════════════════════════════════════════════════"
