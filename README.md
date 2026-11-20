# Language of Computation — Week 6 Assignment (Backend)

A Python backend built with **FastAPI**, using a **PostgreSQL** database that
runs in **Docker**.

- **Student:** Melissa Forte (GitHub: MForte-AI)

## What's in this folder

| File | What it does |
| --- | --- |
| `app/main.py` | The FastAPI app and its endpoints (`/` and `/health`) |
| `app/database.py` | Connects to PostgreSQL with SQLAlchemy |
| `app/config.py` | Reads settings, like the database address, from `.env` |
| `docker-compose.yml` | Runs PostgreSQL in a Docker container |
| `.env.example` | Sample settings. Copy it to `.env` (which git ignores) |
| `requirements.txt` | The Python packages the app needs |
| `tests/test_main.py` | Tests for the endpoints (they don't need the database) |

## How to run it

### 1. Install Docker Desktop (first time only)
Download it from <https://www.docker.com/products/docker-desktop/>, open it,
and wait until it says Docker is running.

### 2. Go to the project folder
```bash
cd ~/workspace/language-of-computation/week6-assignment-backend
```

### 3. Create your settings file (first time only)
```bash
cp .env.example .env
```

### 4. Start the database
```bash
docker compose up -d
```
`-d` runs it in the background. To check that it's ready:
```bash
docker compose ps
```
The `STATUS` column should say `healthy`.

### 5. Set up Python (first time only)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```
Next time, you only need `source .venv/bin/activate`.

### 6. Start the app
```bash
fastapi dev app/main.py
```
Then open:
- <http://127.0.0.1:8000/> for a welcome message
- <http://127.0.0.1:8000/health> to check the database connection.
  It shows `"database": "connected"` when Postgres is running.
- <http://127.0.0.1:8000/docs> for interactive API docs

Press **Control + C** to stop the app.

## How to run the tests
```bash
source .venv/bin/activate
python -m pytest -v
```

## Stopping the database
```bash
docker compose down
```
Your data is kept in a Docker volume called `postgres_data`. To delete the
data too, run `docker compose down -v`.
