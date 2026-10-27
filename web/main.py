"""
FastAPI app — two-player tic-tac-toe (hot seat).

Run: uvicorn main:app --reload --port 3021
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

_DEMO_ROOT = Path(__file__).resolve().parent.parent
if str(_DEMO_ROOT) not in sys.path:
    sys.path.insert(0, str(_DEMO_ROOT))

from ttt_core import apply_move, initial_state, state_for_client  # noqa: E402

app = FastAPI(title="Tic-Tac-Toe")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")


class BoardModel(BaseModel):
    board: dict[str, str | None]


class GameStateModel(BaseModel):
    board: dict[str, str | None]
    current_player: Literal["X", "O"]
    status: Literal["playing", "won", "tie"] = "playing"
    winner: Literal["X", "O"] | None = None


def _board_to_internal(board: dict[str, str | None]) -> dict[str, str]:
    internal: dict[str, str] = {}
    for space in "123456789":
        value = board.get(space)
        internal[space] = value if value in ("X", "O") else " "
    return internal


def _state_from_client(body: GameStateModel) -> dict:
    return {
        "board": _board_to_internal(body.board),
        "current_player": body.current_player,
        "status": body.status,
        "winner": body.winner,
    }


class MoveRequest(BaseModel):
    state: GameStateModel
    space: str = Field(..., pattern=r"^[1-9]$")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html")


@app.get("/help", response_class=HTMLResponse)
async def help_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "help.html")


@app.post("/api/reset")
async def api_reset() -> JSONResponse:
    return JSONResponse(state_for_client(initial_state()))


@app.post("/api/move")
async def api_move(body: MoveRequest) -> JSONResponse:
    try:
        state = _state_from_client(body.state)
        new_state = apply_move(state, body.space)
        return JSONResponse(state_for_client(new_state))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
