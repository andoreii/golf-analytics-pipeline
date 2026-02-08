# Golf Statistics ETL + Analytics Dashboard

End-to-end ETL data pipeline for personal golf stats using PostgreSQL, dbt-core, and Streamlit.

## What this project does
- Collects round-by-round stats from Excel
- Loads data into PostgreSQL
- Transforms and models data with dbt
- Presents insights in a Streamlit analytics dashboard
- Includes a Streamlit mini app to add courses, tees, and hole yardages

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
See `docs/PROJECT_OVERVIEW.md` for recruiter-facing project details.
