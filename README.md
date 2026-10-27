# Tic-Tac-Toe (catalog #518)

Al Sweigart — *The Big Book of Small Python Projects*, Project #76.

| Artifact | Path |
|----------|------|
| Book steps | [`BOOK_DIRECTIONS.md`](./BOOK_DIRECTIONS.md) |
| Upstream script | [`reference/tictactoe.py`](./reference/tictactoe.py) |
| CLI | [`reference/run_cli.py`](./reference/run_cli.py) |
| Shared logic | [`ttt_core.py`](./ttt_core.py) |
| Web (FastAPI) | [`web/`](./web/) — port **3021** |

## Run the web demo

```powershell
Set-Location "c:\Users\emmak\Desktop\Content\CodingProjects\PortProjects\demos\tic-tac-toe\web"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 3021
```

Open [http://127.0.0.1:3021/](http://127.0.0.1:3021/).

## Run the CLI

```powershell
Set-Location "c:\Users\emmak\Desktop\Content\CodingProjects\PortProjects\demos\tic-tac-toe"
python reference\run_cli.py
```

Portfolio: [`PORTFOLIO_INTEGRATION.md`](./PORTFOLIO_INTEGRATION.md).
