const turnText = document.getElementById("turn-text");
const resultText = document.getElementById("result-text");
const errorEl = document.getElementById("error-text");
const newBtn = document.getElementById("btn-new");
const cells = document.querySelectorAll(".cell");

const SESSION_KEY = "tic-tac-toe-v1";

let state = null;

function persistState() {
  if (state) AppSession.save(SESSION_KEY, state);
}

function restoreState() {
  const saved = AppSession.load(SESSION_KEY);
  if (!saved?.board) return false;
  state = saved;
  render();
  return true;
}

AppSession.wireHelpSave(SESSION_KEY, () => state);

function setError(message) {
  errorEl.hidden = !message;
  errorEl.textContent = message || "";
}

function render() {
  if (!state) return;
  cells.forEach((cell) => {
    const space = cell.dataset.space;
    const mark = state.board[space];
    cell.textContent = mark || "";
    cell.classList.toggle("is-x", mark === "X");
    cell.classList.toggle("is-o", mark === "O");
    const playable = state.status === "playing" && !mark;
    cell.disabled = !playable;
  });

  if (state.status === "playing") {
    turnText.hidden = false;
    turnText.textContent = `${state.current_player}'s turn`;
    resultText.hidden = true;
  } else {
    turnText.hidden = true;
    resultText.hidden = false;
    if (state.status === "won") {
      resultText.textContent = `${state.winner} wins!`;
      resultText.className = "result-text is-win";
    } else {
      resultText.textContent = "It's a tie!";
      resultText.className = "result-text is-tie";
    }
  }
}

async function resetGame() {
  setError(null);
  try {
    const res = await fetch("/api/reset", { method: "POST" });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Could not reset.");
    AppSession.clear(SESSION_KEY);
    state = data;
    render();
    persistState();
  } catch (err) {
    setError(err.message || "Could not reset.");
  }
}

async function playSpace(space) {
  if (!state || state.status !== "playing") return;
  setError(null);
  try {
    const res = await fetch("/api/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ state, space }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || "Invalid move.");
    state = data;
    render();
    persistState();
  } catch (err) {
    setError(err.message || "Invalid move.");
  }
}

cells.forEach((cell) => {
  cell.addEventListener("click", () => playSpace(cell.dataset.space));
});

newBtn.addEventListener("click", () => resetGame());

if (!restoreState()) resetGame();
