"""
visual_replay.py — Browser-based Snake AI visualization for demos

Generates an HTML file with animated replay of the current AI playing.
Opens automatically in the browser.

Usage:
    python visual_replay.py                # play all 10 seeds, open in browser
    python visual_replay.py --seed 100     # specific seed
    python visual_replay.py --speed 80     # ms per frame (default: 100)
    python visual_replay.py --all          # record all 10 games, pick best
"""

import sys
import json
import os
import subprocess
from snake_engine import SnakeGame, Direction

DEFAULT_SPEED = 100  # ms per frame


def record_game(seed: int) -> dict:
    """Record a full game as a list of frames."""
    game = SnakeGame(width=20, height=20, seed=seed)

    try:
        from target import decide
    except Exception as e:
        return {"seed": seed, "error": str(e), "frames": [], "score": 0}

    frames = []
    last_score = 0
    steps_since_food = 0

    # Record initial frame
    frames.append({
        "snake": [(p.x, p.y) for p in game.snake],
        "food": (game.food.x, game.food.y),
        "score": game.score,
        "steps": game.steps,
        "alive": True,
    })

    while not game.game_over:
        state = game.get_state()

        try:
            action = decide(state)
        except Exception:
            break

        if not isinstance(action, Direction):
            break

        alive, score = game.step(action)

        if score > last_score:
            steps_since_food = 0
            last_score = score
        else:
            steps_since_food += 1

        if steps_since_food > 200:
            break

        frames.append({
            "snake": [(p.x, p.y) for p in game.snake],
            "food": (game.food.x, game.food.y),
            "score": game.score,
            "steps": game.steps,
            "alive": alive,
        })

    return {
        "seed": seed,
        "frames": frames,
        "score": game.score,
        "steps": game.steps,
        "error": None,
    }


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>🐍 Snake AI — AutoResearch Demo</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #0d1117;
    color: #e6edf3;
    font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', monospace;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
  }
  h1 {
    font-size: 28px;
    margin-bottom: 8px;
    background: linear-gradient(90deg, #58a6ff, #3fb950, #f0883e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .subtitle {
    color: #8b949e;
    font-size: 14px;
    margin-bottom: 20px;
  }
  .game-container {
    display: flex;
    gap: 24px;
    align-items: flex-start;
  }
  canvas {
    border: 2px solid #30363d;
    border-radius: 8px;
    box-shadow: 0 0 40px rgba(56, 139, 253, 0.15);
  }
  .sidebar {
    width: 260px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .stat-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 16px;
  }
  .stat-card h3 {
    font-size: 12px;
    text-transform: uppercase;
    color: #8b949e;
    letter-spacing: 1px;
    margin-bottom: 8px;
  }
  .stat-value {
    font-size: 36px;
    font-weight: bold;
  }
  .score-value { color: #3fb950; }
  .steps-value { color: #58a6ff; }
  .length-value { color: #f0883e; }
  .seed-value { color: #bc8cff; }
  .controls {
    display: flex;
    gap: 8px;
    margin-top: 4px;
  }
  button {
    background: #21262d;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 8px 16px;
    font-family: inherit;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s;
  }
  button:hover { background: #30363d; border-color: #58a6ff; }
  button.active { background: #1f6feb; border-color: #58a6ff; }
  .speed-control {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: #8b949e;
  }
  input[type="range"] {
    width: 120px;
    accent-color: #58a6ff;
  }
  .game-selector {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
  }
  .game-btn {
    width: 40px;
    height: 32px;
    font-size: 11px;
    padding: 0;
    text-align: center;
  }
  .game-btn.best { border-color: #3fb950; color: #3fb950; }
  .status-bar {
    margin-top: 16px;
    padding: 12px 20px;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    font-size: 13px;
    color: #8b949e;
    text-align: center;
    min-width: 600px;
  }
  .status-bar .highlight { color: #3fb950; font-weight: bold; }
</style>
</head>
<body>

<h1>🐍 Snake AI — AutoResearch Demo</h1>
<p class="subtitle">Watching the AI play • Bob Shell optimizes this autonomously</p>

<div class="game-container">
  <canvas id="board" width="500" height="500"></canvas>
  <div class="sidebar">
    <div class="stat-card">
      <h3>🎯 Score</h3>
      <div class="stat-value score-value" id="score">0</div>
    </div>
    <div class="stat-card">
      <h3>👣 Steps</h3>
      <div class="stat-value steps-value" id="steps">0</div>
    </div>
    <div class="stat-card">
      <h3>🐍 Length</h3>
      <div class="stat-value length-value" id="length">3</div>
    </div>
    <div class="stat-card">
      <h3>🎲 Seed</h3>
      <div class="stat-value seed-value" id="seed">-</div>
    </div>
    <div class="stat-card">
      <h3>Controls</h3>
      <div class="controls">
        <button id="playBtn" class="active" onclick="togglePlay()">⏸ Pause</button>
        <button onclick="restart()">🔄 Restart</button>
      </div>
      <div class="speed-control" style="margin-top: 10px;">
        <span>🐢</span>
        <input type="range" id="speedSlider" min="20" max="300" value="SPEED_PLACEHOLDER" oninput="updateSpeed(this.value)">
        <span>🐇</span>
      </div>
    </div>
    <div class="stat-card">
      <h3>Games</h3>
      <div class="game-selector" id="gameSelector"></div>
    </div>
  </div>
</div>

<div class="status-bar" id="statusBar">
  Loading...
</div>

<script>
const CELL = 25;
const GAMES = GAMES_PLACEHOLDER;
const canvas = document.getElementById('board');
const ctx = canvas.getContext('2d');

let currentGame = 0;
let frameIdx = 0;
let playing = true;
let speed = SPEED_PLACEHOLDER;
let intervalId = null;

// Find best game
const bestIdx = GAMES.reduce((best, g, i) => g.score > GAMES[best].score ? i : best, 0);

// Build game selector
const selector = document.getElementById('gameSelector');
GAMES.forEach((g, i) => {
  const btn = document.createElement('button');
  btn.className = 'game-btn' + (i === bestIdx ? ' best' : '');
  btn.textContent = `#${i}`;
  btn.title = `Seed ${g.seed} — Score: ${g.score}`;
  btn.onclick = () => loadGame(i);
  selector.appendChild(btn);
});

function loadGame(idx) {
  currentGame = idx;
  frameIdx = 0;
  document.getElementById('seed').textContent = GAMES[idx].seed;
  document.querySelectorAll('.game-btn').forEach((b, i) => {
    b.style.background = i === idx ? '#1f6feb' : '';
  });
  if (playing) startInterval();
  else drawFrame();
}

function drawFrame() {
  const game = GAMES[currentGame];
  const frame = game.frames[frameIdx];
  if (!frame) return;

  const w = 20, h = 20;
  ctx.fillStyle = '#0d1117';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Grid
  ctx.strokeStyle = '#161b22';
  ctx.lineWidth = 0.5;
  for (let x = 0; x <= w; x++) {
    ctx.beginPath(); ctx.moveTo(x*CELL, 0); ctx.lineTo(x*CELL, h*CELL); ctx.stroke();
  }
  for (let y = 0; y <= h; y++) {
    ctx.beginPath(); ctx.moveTo(0, y*CELL); ctx.lineTo(w*CELL, y*CELL); ctx.stroke();
  }

  // Food — pulsing red
  const pulse = 0.8 + 0.2 * Math.sin(frameIdx * 0.3);
  const foodR = CELL/2 * pulse;
  ctx.fillStyle = '#f85149';
  ctx.shadowColor = '#f85149';
  ctx.shadowBlur = 12;
  ctx.beginPath();
  ctx.arc(frame.food[0]*CELL + CELL/2, frame.food[1]*CELL + CELL/2, foodR, 0, Math.PI*2);
  ctx.fill();
  ctx.shadowBlur = 0;

  // Snake body
  const snake = frame.snake;
  for (let i = snake.length - 1; i >= 0; i--) {
    const [sx, sy] = snake[i];
    const t = i / Math.max(snake.length - 1, 1);

    if (i === 0) {
      // Head — bright green with glow
      ctx.fillStyle = '#3fb950';
      ctx.shadowColor = '#3fb950';
      ctx.shadowBlur = 8;
      ctx.beginPath();
      ctx.roundRect(sx*CELL+1, sy*CELL+1, CELL-2, CELL-2, 4);
      ctx.fill();
      ctx.shadowBlur = 0;

      // Eyes
      ctx.fillStyle = '#0d1117';
      const dir = frameIdx > 0 ? getDir(snake, GAMES[currentGame].frames[Math.max(0,frameIdx-1)].snake) : [1,0];
      const ex1 = sx*CELL + CELL/2 + dir[1]*3 - dir[0]*3;
      const ey1 = sy*CELL + CELL/2 - dir[0]*3 - dir[1]*3;
      const ex2 = sx*CELL + CELL/2 + dir[1]*3 + dir[0]*3;
      const ey2 = sy*CELL + CELL/2 - dir[0]*3 + dir[1]*3;
      ctx.beginPath(); ctx.arc(ex1, ey1, 2, 0, Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.arc(ex2, ey2, 2, 0, Math.PI*2); ctx.fill();
    } else {
      // Body — gradient from green to darker
      const g = Math.floor(185 - t * 100);
      const b = Math.floor(80 - t * 50);
      ctx.fillStyle = `rgb(${30+t*10}, ${g}, ${b})`;
      ctx.beginPath();
      ctx.roundRect(sx*CELL+2, sy*CELL+2, CELL-4, CELL-4, 3);
      ctx.fill();
    }
  }

  // Update stats
  document.getElementById('score').textContent = frame.score;
  document.getElementById('steps').textContent = frame.steps;
  document.getElementById('length').textContent = snake.length;

  // Status
  const pct = ((frameIdx / Math.max(game.frames.length-1, 1)) * 100).toFixed(0);
  const alive = frame.alive ? '🟢 Alive' : '💀 Dead';
  document.getElementById('statusBar').innerHTML =
    `${alive} &nbsp;|&nbsp; Frame ${frameIdx+1}/${game.frames.length} (${pct}%) &nbsp;|&nbsp; ` +
    `Best game: <span class="highlight">#${bestIdx} (score: ${GAMES[bestIdx].score})</span> &nbsp;|&nbsp; ` +
    `Avg: <span class="highlight">${(GAMES.reduce((s,g)=>s+g.score,0)/GAMES.length).toFixed(1)}</span>`;
}

function getDir(snakeNow, snakePrev) {
  if (!snakePrev || snakePrev.length === 0) return [1, 0];
  const [hx, hy] = snakeNow[0];
  const [px, py] = snakePrev[0];
  const dx = hx - px, dy = hy - py;
  if (dx === 0 && dy === 0) return [1, 0];
  return [dx, dy];
}

function tick() {
  const game = GAMES[currentGame];
  if (frameIdx >= game.frames.length - 1) {
    // Auto-advance to next game
    if (currentGame < GAMES.length - 1) {
      loadGame(currentGame + 1);
    } else {
      loadGame(0); // loop
    }
    return;
  }
  frameIdx++;
  drawFrame();
}

function togglePlay() {
  playing = !playing;
  document.getElementById('playBtn').textContent = playing ? '⏸ Pause' : '▶ Play';
  document.getElementById('playBtn').className = playing ? 'active' : '';
  if (playing) startInterval();
  else clearInterval(intervalId);
}

function restart() {
  frameIdx = 0;
  if (!playing) drawFrame();
}

function updateSpeed(val) {
  speed = 320 - val; // invert so right = faster
  if (playing) startInterval();
}

function startInterval() {
  clearInterval(intervalId);
  intervalId = setInterval(tick, speed);
}

// Start
loadGame(bestIdx);
startInterval();
</script>
</body>
</html>"""


def main():
    speed = DEFAULT_SPEED
    seeds_to_run = list(range(100, 110))
    specific_seed = None

    args = sys.argv[1:]
    if "--speed" in args:
        idx = args.index("--speed")
        speed = int(args[idx + 1])
    if "--seed" in args:
        idx = args.index("--seed")
        specific_seed = int(args[idx + 1])
        seeds_to_run = [specific_seed]

    print("🐍 Recording Snake AI games...")

    games = []
    for seed in seeds_to_run:
        result = record_game(seed)
        games.append(result)
        print(f"  seed={seed}  score={result['score']:>3}  frames={len(result['frames'])}")

    # Build JSON data (compact)
    games_json = json.dumps([{
        "seed": g["seed"],
        "score": g["score"],
        "steps": g["steps"],
        "frames": g["frames"],
    } for g in games])

    html = HTML_TEMPLATE.replace("GAMES_PLACEHOLDER", games_json)
    html = html.replace("SPEED_PLACEHOLDER", str(speed))

    out_path = os.path.join(os.path.dirname(__file__), "replay.html")
    with open(out_path, "w") as f:
        f.write(html)

    print(f"\n✅ Saved to {out_path}")
    avg = sum(g["score"] for g in games) / len(games)
    best = max(g["score"] for g in games)
    print(f"   Avg score: {avg:.1f}  |  Best: {best}")

    # Try to open in browser
    try:
        subprocess.run(["xdg-open", out_path], capture_output=True, timeout=3)
        print("   Opened in browser 🌐")
    except Exception:
        print(f"   Open manually: file://{os.path.abspath(out_path)}")


if __name__ == "__main__":
    main()
