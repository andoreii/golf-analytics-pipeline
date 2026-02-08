# Setup (notes to future me)

## 1) Get PostgreSQL running
Pick one:

Option A — Homebrew (fast on macOS)
- `brew install postgresql@16`
- `brew services start postgresql@16`
- `createdb golf_stats`

Option B — Docker (clean + isolated)
- Install Docker Desktop
- Run:
  - `docker run --name golf-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=golf_stats -p 5432:5432 -d postgres:16`

## 2) Python setup
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`

## 3) dbt (for the models)
- `pip install dbt-core==1.8.2 dbt-postgres==1.8.2`

## 4) Environment variables
Create a `.env` file in the project root:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=golf_stats
DB_USER=postgres
DB_PASSWORD=postgres
```

## 5) Create tables
Run the SQL in `db/migrations/` in order:
- `001_create_tables.sql`
- `002_create_tee_holes.sql`
- `003_add_round_external_id.sql`

## 6) dbt profile
Copy `dbt/profiles.yml.example` to `~/.dbt/profiles.yml` and update creds if needed.

## 7) Run the app
- `streamlit run streamlit_app/app.py`

## 8) Load data (when ready)
- Put the Excel file in `data/raw/`
- Run: `python scripts/ingest_excel.py`
