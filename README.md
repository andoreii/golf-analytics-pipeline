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

