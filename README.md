# Language of Computation — Week 6 Assignment (Backend)

A Python backend built with **FastAPI**, using a **PostgreSQL** database that
runs in **Docker**. The frontend team runs it on their own computers at
`http://127.0.0.1:8000`.

- **Student:** Melissa Forte (GitHub: MForte-AI)

> **Frontend teammates:** you don't need to read the rest of this file. Open
> Claude Code and say:
>
> *"Clone https://github.com/MForte-AI/language-of-computation-week6-assignment-backend
> and follow its README.md to run the backend on localhost."*
>
> Claude will ask you before it installs anything or deletes data.

## Quick facts

| What | Value |
| --- | --- |
| API base URL | `http://127.0.0.1:8000` (`http://localhost:8000` also works in a browser) |
| Interactive API docs | `http://127.0.0.1:8000/docs` |
| OpenAPI schema (for generating frontend types) | `http://127.0.0.1:8000/openapi.json` |
| Health check | `GET /health` returns `{"status":"ok","database":"connected"}` |
| Frontend origins allowed by CORS | `http://localhost:5173`, `http://127.0.0.1:5173`, `http://localhost:3000`, `http://127.0.0.1:3000` |
| PostgreSQL | `localhost:5432`, database `week6`, user `week6`, password `week6_dev_password` (local development only) |
| Python | 3.11 or newer |

---

## Instructions for Claude

You are setting up this backend on a teammate's Mac or Windows computer so
their frontend can call it on localhost. Work through the steps in order and
run each step's check before moving on. If a check fails, use
[Troubleshooting](#troubleshooting).

### Ground rules

- **Ask the user before installing system software** (Docker Desktop, Python).
  Docker Desktop needs the user's admin password and license acceptance, so
  the user must install it themselves. Give them the link and wait.
- **Never run `docker compose down -v`** or delete the `postgres_data` volume
  unless the user agrees. It permanently erases the database.
- **Never commit or push.** This is local setup only. `.env` must never be
  committed (git already ignores it).
- **If you change a port, tell the user the new URL** so the frontend can be
  pointed at it.
- Shell state doesn't carry between your commands, so **don't activate the
  virtual environment**. Call its Python directly (see the table below).

### Mac and Windows differences

Commands below are written for **bash**: zsh/bash on macOS, or **Git Bash**
on Windows, which is the shell Claude Code uses there. Swap in the right value
from this table. For PowerShell, see
[PowerShell versions of the commands](#powershell-versions-of-the-commands).

| | macOS | Windows (Git Bash) |
| --- | --- | --- |
| `$PYTHON` (to create the venv) | `python3` | `py -3` (if `py` is missing, `python`) |
| `$VENV_PY` (the project's Python) | `.venv/bin/python` | `.venv/Scripts/python.exe` |
| Start Docker Desktop | `open -a Docker` | `powershell.exe -NoProfile -Command "Start-Process 'C:\Program Files\Docker\Docker\Docker Desktop.exe'"` |

### Step 1: Get the code

If the folder isn't already on this computer:
```bash
git clone https://github.com/MForte-AI/language-of-computation-week6-assignment-backend.git
cd language-of-computation-week6-assignment-backend
```
If it is, `cd` into it and run `git pull` to get the latest version.

**Check:** `docker-compose.yml`, `requirements.txt` and an `app/` folder are
in the current folder.

### Step 2: Check the prerequisites

```bash
git --version
docker --version
docker compose version
$PYTHON --version
```

**Check:**
- `docker` prints a version. If it's not found, Docker Desktop isn't
  installed. Stop and ask the user to install it from
  <https://www.docker.com/products/docker-desktop/>. On Windows it uses WSL 2
  and may need a restart.
- `docker compose version` is v2.17 or newer (needed for `--wait` below).
  Any v3, v4, v5 or later is fine.
- Python is **3.11 or newer**. If not, ask the user to install it from
  <https://www.python.org/downloads/>. On Windows, `py --list` shows every
  installed version, and `py -3.13` picks a specific one.

### Step 3: Make sure Docker is running

```bash
docker info > /dev/null 2>&1 && echo "Docker is running" || echo "Docker is NOT running"
```
If it's not running, start Docker Desktop with the command from the table, then
wait for it (this can take up to a minute):
```bash
for i in $(seq 1 60); do docker info > /dev/null 2>&1 && echo "Docker is running" && break; sleep 2; done
```

**Check:** prints `Docker is running`.

### Step 4: Create the settings file

Only if `.env` doesn't exist yet. Never overwrite an existing one, because the
user may have changed it.
```bash
[ -f .env ] || cp .env.example .env
```

**Check:** `.env` exists.

### Step 5: Start PostgreSQL

```bash
docker compose up -d --wait
```
`-d` runs it in the background. `--wait` returns only once the database passes
its health check. The first run downloads the `postgres:17` image, which can
take a few minutes.

**Check:** `docker compose ps` shows `week6-postgres` with status `healthy`.

### Step 6: Set up Python

Create the virtual environment only if `.venv` doesn't exist yet, then install
the packages (safe to re-run):
```bash
[ -d .venv ] || $PYTHON -m venv .venv
$VENV_PY -m pip install -r requirements.txt
```

**Check:** the install ends without errors.

### Step 7: Run the tests

```bash
$VENV_PY -m pytest -q
```

**Check:** `5 passed`.

### Step 8: Start the API

This command **keeps running until it's stopped**, so start it as a
**background process** and don't wait for it to finish:
```bash
$VENV_PY -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
`--reload` restarts the server automatically when a `.py` file changes. The
first start can take 10 to 20 seconds.

### Step 9: Confirm it works

```bash
curl -s http://127.0.0.1:8000/health
```
If you get no response, the server is still starting. Wait a few seconds and
try again.

**Check:** the response is exactly `{"status":"ok","database":"connected"}`.
Then confirm the browser will accept calls from the frontend:
```bash
curl -s -i -H "Origin: http://localhost:5173" http://127.0.0.1:8000/ | grep -i access-control-allow-origin
```
**Check:** prints `access-control-allow-origin: http://localhost:5173`.

### Step 10: Report to the user

Tell the user:
- The API is running at `http://127.0.0.1:8000`, with docs at `/docs`.
- Which frontend origins are allowed. If their frontend runs on a port not in
  [Quick facts](#quick-facts), follow the CORS fix in
  [Troubleshooting](#troubleshooting).
- How to stop it (see [Stopping](#stopping)).

### Starting again another day

Steps 1 to 7 are one-time setup. Next time, run **Step 3** (Docker running),
**Step 5** (database up), **Step 8** (API) and **Step 9** (confirm). Also run
`git pull` and repeat the install part of **Step 6** in case the
requirements changed.

---

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `docker: command not found` | Docker Desktop isn't installed | The user must install it: <https://www.docker.com/products/docker-desktop/>. Stop and ask. |
| Mac: `docker: command not found`, but `/Applications/Docker.app` exists | Docker Desktop has never been opened, or it put `docker` in `~/.docker/bin` and the current terminal started before that folder was added to `PATH` | Open Docker Desktop (`open -a Docker`) and finish its setup. Then the user opens a **new** terminal window. For your own commands in an already-open session, call `~/.docker/bin/docker` by its full path. |
| `Cannot connect to the Docker daemon` (Mac) or `error during connect ... dockerDesktopLinuxEngine` (Windows) | Docker Desktop isn't running | Step 3 |
| `port is already allocated` or `address already in use` for **5432** | Another PostgreSQL is already running on this computer | In `.env`, set `POSTGRES_PORT=5433` and change `:5432/` to `:5433/` in `DATABASE_URL`. Run `docker compose up -d --wait` again, then restart the API. |
| `address already in use` for **8000** | Something else uses port 8000 | Start the API with `--port 8001` and tell the user the new URL. |
| `/health` returns `{"detail":"Database unavailable"}` | The API is up but can't reach Postgres | Run `docker compose ps` (should show `healthy`). Check `docker compose logs db` and confirm `DATABASE_URL` matches the `POSTGRES_*` values in `.env`. |
| `password authentication failed for user "week6"` | The database was first created with different `.env` values. Postgres only reads `POSTGRES_*` the first time. | Put the original values back in `.env`. Or, **only if the user agrees to erase the local data**, run `docker compose down -v` then `docker compose up -d --wait`. |
| Browser console: `blocked by CORS policy` | The frontend's origin isn't on the allowed list | Add a line to `.env` listing every origin the frontend uses, e.g. `CORS_ORIGINS=["http://localhost:5173","http://localhost:4200"]`, then **restart the API** (`--reload` doesn't watch `.env`). |
| `No matching distribution found` or `requires a different Python` during install | Python is older than 3.11 | Install Python 3.11+, delete `.venv`, repeat Step 6. |
| Windows: `python` opens the Microsoft Store or says `Python was not found` | That's a Windows placeholder, not real Python | Use `py -3`, or install Python from python.org. |
| Windows PowerShell: `running scripts is disabled on this system` | Venv activation scripts are blocked | You don't need activation. Call `.venv\Scripts\python.exe` directly. |
| Node-side requests (a Vite proxy or Next.js server code) to `localhost:8000` get `ECONNREFUSED` | Node tried the IPv6 address `::1` first, and the API listens on IPv4 | Use `http://127.0.0.1:8000` instead of `localhost`. |

---

## Connecting a frontend

- Call the API at `http://127.0.0.1:8000`, for example
  `fetch("http://127.0.0.1:8000/health")`.
- The allowed frontend origins are listed in [Quick facts](#quick-facts). To
  add one, use the CORS fix in [Troubleshooting](#troubleshooting).
- Every endpoint is described at `http://127.0.0.1:8000/docs`, and as JSON at
  `/openapi.json` for tools that generate TypeScript types.

## Stopping

- **API:** stop the background `uvicorn` process (or press **Control + C** in
  its terminal).
- **Database:** `docker compose stop` pauses it. `docker compose down` removes
  the container. Both **keep your data**.
- `docker compose down -v` **erases all data**. Only do this on purpose.

## PowerShell versions of the commands

```powershell
git clone https://github.com/MForte-AI/language-of-computation-week6-assignment-backend.git
cd language-of-computation-week6-assignment-backend
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
docker compose up -d --wait
if (-not (Test-Path .venv)) { py -3 -m venv .venv }
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
In a second PowerShell window (use `curl.exe`, because plain `curl` in
PowerShell is a different command):
```powershell
curl.exe -s http://127.0.0.1:8000/health
```

## What's in this folder

| File | What it does |
| --- | --- |
| `app/main.py` | The FastAPI app, its endpoints (`/` and `/health`) and CORS setup |
| `app/database.py` | Connects to PostgreSQL with SQLAlchemy |
| `app/config.py` | Reads settings (database address, CORS origins) from `.env` |
| `docker-compose.yml` | Runs PostgreSQL 17 in a Docker container |
| `.env.example` | Sample settings. Copy it to `.env` (which git ignores) |
| `requirements.txt` | The Python packages, pinned to tested versions |
| `.gitattributes` | Keeps line endings the same on Mac and Windows |
| `tests/test_main.py` | Tests for the endpoints and CORS (no database needed) |
