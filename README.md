# Golf Statistics ETL + Analytics Dashboard

A personal project to track my golf rounds, model the data cleanly, and surface insights I actually care about.

## What this project does
- Tracks round-by-round stats in a simple Excel template
- Loads that data into PostgreSQL
- Models it with dbt so the analytics are consistent
- Shows the results in a Streamlit dashboard
- Includes a small Streamlit form to add courses/tees/holes

## Project structure
- `db/` PostgreSQL schema, migrations, and seed data
- `dbt/` dbt models and project config
- `scripts/` ETL scripts (Excel -> PostgreSQL)
- `streamlit_app/` dashboard app
- `docs/` setup and project documentation
- `data/` raw and processed files (not committed)

## Getting started
See `docs/SETUP.md` for installation and setup.

## Documentation
See `docs/PROJECT_OVERVIEW.md` for a quick project walk‑through.
See `docs/EXCEL_TEMPLATE.md` for the Excel tracking template.

## Dashboard
Start the dashboard:
```
streamlit run streamlit_app/app.py
```

## How to Run (End-to-End)
1. Start PostgreSQL (Docker)
   ```
   docker run --name golf-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=golf_stats -p 5432:5432 -d postgres:16
   ```
2. Create `.env`
   ```
   cp .env.example .env
   ```
3. Run migrations
   ```
   PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d golf_stats -c "\\i db/migrations/001_create_tables.sql"
   PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d golf_stats -c "\\i db/migrations/002_create_tee_holes.sql"
   PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d golf_stats -c "\\i db/migrations/003_add_round_external_id.sql"
   ```
4. Install Python dependencies
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
5. Configure dbt
   ```
   mkdir -p ~/.dbt
   cp dbt/profiles.yml.example ~/.dbt/profiles.yml
   ```
6. Build dbt models
   ```
   cd dbt
   dbt run
   ```
7. Generate Excel template
   ```
   python scripts/create_excel_template.py
   ```
8. Start Streamlit
   ```
   streamlit run streamlit_app/app.py
   ```
