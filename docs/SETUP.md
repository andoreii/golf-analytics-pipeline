# Setup (PostgreSQL + dbt + Streamlit)

This project is 100% free to run locally. You only need a laptop and an internet connection for installing tools.

## 1) Install PostgreSQL (database)
Choose one option:

Option A — Homebrew (simplest on macOS)
- Install: `brew install postgresql@16`
- Start the database: `brew services start postgresql@16`
- Create a database: `createdb golf_stats`

Option B — Docker (keeps everything self-contained)
- Install Docker Desktop
- Run:
  - `docker run --name golf-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=golf_stats -p 5432:5432 -d postgres:16`

## 2) Install Python + dependencies
- Create a virtual environment:
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`
- Install libraries:
  - `pip install -r requirements.txt`

## 3) Install dbt (data modeling tool)
- `pip install dbt-core==1.8.9 dbt-postgres==1.8.9`

## 4) Configure environment variables
Create a `.env` file in the project root:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=golf_stats
DB_USER=postgres
DB_PASSWORD=postgres
```

## 5) Initialize the database schema
Run all SQL files in `db/migrations/` in order:
- `001_create_tables.sql`
- `002_create_tee_holes.sql`
- `003_add_round_external_id.sql`

## 6) Configure dbt profile
Copy `dbt/profiles.yml.example` to `~/.dbt/profiles.yml` and update your username/password.

## 7) Run the Streamlit app
- `streamlit run streamlit_app/app.py`

## 8) Load data from Excel (when ready)
- Place your Excel file in `data/raw/`
- Run: `python scripts/ingest_excel.py`
