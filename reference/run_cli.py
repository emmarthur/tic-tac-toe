"""Two-player terminal tic-tac-toe — uses shared ttt_core logic."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from ttt_core import apply_move, board_display, initial_state  # noqa: E402

print("Welcome to Tic-Tac-Toe!")

state = initial_state()

while state["status"] == "playing":
    print(board_display(state["board"]))
    player = state["current_player"]
    move = None
    while True:
        raw = input(f"What is {player}'s move? (1-9)\n> ").strip()
        try:
            state = apply_move(state, raw)
            break
        except ValueError as exc:
            print(exc)

print(board_display(state["board"]))
if state["status"] == "won":
    print(f"{state['winner']} has won the game!")
else:
    print("The game is a tie!")
print("Thanks for playing!")
