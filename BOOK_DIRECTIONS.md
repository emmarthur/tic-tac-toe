# Book directions — Tic-Tac-Toe

**Catalog #518** · Al Sweigart, *The Big Book of Small Python Projects*, **Project #76** — Tic-Tac-Toe

- Invent with Python: [project76.html](https://inventwithpython.com/bigbookpython/project76.html)
- Upstream: [tictactoe.py](https://github.com/asweigart/the-big-book-of-small-python-projects/blob/main/tictactoe.py)
- Local reference: [`reference/tictactoe.py`](./reference/tictactoe.py)
- Shared logic: [`ttt_core.py`](./ttt_core.py)

## What the book asks you to build

A **two-player** terminal game:

1. Board as a **dictionary** with keys `'1'`–`'9'` and values `X`, `O`, or blank.
2. **X** moves first; players alternate entering a space number.
3. Reject invalid or occupied spaces until a legal move is entered.
4. Detect **eight winning lines** or a **full-board tie**.
5. Print the ASCII board after each turn.

## Web version (`web/` — FastAPI, port **3021**)

| Book step | Web equivalent |
|-----------|----------------|
| Dictionary board | `ttt_core.blank_board` / `apply_move` |
| Alternate X and O | Hot-seat: two players share one screen |
| Spaces 1–9 | 3×3 grid buttons (same numbering as help page) |
| Win / tie | `status` + `winner` in API JSON |
| New match | `POST /api/reset` |

CLI: [`reference/run_cli.py`](./reference/run_cli.py)
