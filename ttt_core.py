"""
Tic-tac-toe board logic — shared by CLI and web.

Follows Al Sweigart's dictionary board (spaces 1–9), X and O, and win detection.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Literal

ALL_SPACES: tuple[str, ...] = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
Player = Literal["X", "O"]
BLANK = " "


def blank_board() -> dict[str, str]:
    return {space: BLANK for space in ALL_SPACES}


def initial_state() -> dict[str, Any]:
    return {"board": blank_board(), "current_player": "X", "status": "playing"}


def is_valid_space(board: dict[str, str], space: str) -> bool:
    return space in ALL_SPACES and board.get(space) == BLANK


def is_winner(board: dict[str, str], player: str) -> bool:
    b, p = board, player
    return (
        (b["1"] == b["2"] == b["3"] == p)
        or (b["4"] == b["5"] == b["6"] == p)
        or (b["7"] == b["8"] == b["9"] == p)
        or (b["1"] == b["4"] == b["7"] == p)
        or (b["2"] == b["5"] == b["8"] == p)
        or (b["3"] == b["6"] == b["9"] == p)
        or (b["3"] == b["5"] == b["7"] == p)
        or (b["1"] == b["5"] == b["9"] == p)
    )


def is_board_full(board: dict[str, str]) -> bool:
    return all(board[space] != BLANK for space in ALL_SPACES)


def board_for_client(board: dict[str, str]) -> dict[str, str | None]:
    """Map blank spaces to null for JSON."""
    return {
        space: (mark if mark != BLANK else None) for space, mark in board.items()
    }


def state_for_client(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "board": board_for_client(state["board"]),
        "current_player": state["current_player"],
        "status": state["status"],
        "winner": state.get("winner"),
    }


def apply_move(state: dict[str, Any], space: str) -> dict[str, Any]:
    if state.get("status") != "playing":
        raise ValueError("Game is over. Start a new game.")

    board = deepcopy(state["board"])
    player = state["current_player"]

    if not is_valid_space(board, space):
        raise ValueError("That space is not available.")

    board[space] = player
    next_state: dict[str, Any] = {
        "board": board,
        "current_player": "O" if player == "X" else "X",
        "status": "playing",
    }

    if is_winner(board, player):
        next_state["status"] = "won"
        next_state["winner"] = player
        return next_state

    if is_board_full(board):
        next_state["status"] = "tie"
        next_state["winner"] = None
        return next_state

    return next_state


def board_display(board: dict[str, str]) -> str:
    return """
      {}|{}|{}  1 2 3
      -+-+-
      {}|{}|{}  4 5 6
      -+-+-
      {}|{}|{}  7 8 9""".format(
        board["1"],
        board["2"],
        board["3"],
        board["4"],
        board["5"],
        board["6"],
        board["7"],
        board["8"],
        board["9"],
    )
