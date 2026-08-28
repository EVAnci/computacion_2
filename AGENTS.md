# AGENTS.md

## Repo Shape
- This is a Python coursework repo, not a single installable package. Work inside the relevant subdirectory (`TP1`, `TP2`, `Clases`, etc.) so relative imports and generated files land in the expected place.
- No root package manifest, CI workflow, formatter, lint config, or pre-commit config was found; do not invent npm/poetry/ruff flows.

## Course Context
- `Clases/` contains theory notes, exercises, and small demos for Computación II; use it as subject-matter context, not as one cohesive application.
- The recurring themes are concurrent systems, multiprocessing/threading, process communication (`pipes`, `fifo`, `queue`, signals), sockets/TCP/UDP/IPv4/IPv6, async Python (`asyncio`, `aiohttp`, `concurrent.futures`), and operating-systems concepts around processes and memory.
- Some class materials are exploratory notes or prompts; prefer runnable `.py` files and TP READMEs when deciding how code is actually wired.

## TP1
- Entrypoints must be run from `TP1/` because imports use `src.*` and files like `blockchain.json`/`reporte.txt` are relative to the current directory.
- Run the main multiprocessing simulation with `python3 main.py`; useful flags are `-n/--num` (default `60`) and `-v/--verbose`.
- Generate/validate the report with `python3 verificar_cadena.py`; it reads `blockchain.json` and writes `reporte.txt` in `TP1/`.
- Tests are `unittest` tests under `TP1/tests/`; run all with `python3 -m unittest discover -s tests` from `TP1/`, or one file with `python3 -m unittest tests.test_generador`.
- TP1 imports `numpy` directly but has no local requirements file; install it separately if the environment lacks it.

## TP2
- Install runtime deps from `TP2/requirements.txt`, typically from `TP2/` with `python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt`.
- `pyrightconfig.json` points at a hard-coded `.venv` path containing `Computación 2` while this repo path contains `Computación II`; fix that path before relying on Pyright results.
- Server B (`server_processing.py`) is the TCP/Selenium processing server. Start it before Server A, for example: `python server_processing.py -i 127.0.0.2 -p 8000`.
- Server A (`server_scraping.py`) is the aiohttp `/scrape` server. Example matching the docs/client defaults: `python server_scraping.py -i ::1 -p 8080`; if Server B uses non-default address/port pass `-b/--b_ip` and `-d/--b_port`.
- The client defaults to Server A at `[::1]:8080`; use `python client.py -t` for the built-in 10 test URLs, or `python client.py https://example.com` for focused testing.
- TP2 writes client results under `TP2/pages/<domain>/` with decoded images in `media/`; bash helper scripts also write under `pages/` and assume Server A is on `localhost:8080`.
- Selenium uses headless Chrome via `webdriver.Chrome`; TP2 processing requires a compatible Chrome/Chromedriver available in the environment, not just Python packages.
- Server A and B communicate using a custom 4-byte big-endian length header plus JSON body in `common/protocol.py`; keep that framing in sync on both sides.
