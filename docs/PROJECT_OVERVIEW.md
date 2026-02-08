# Project Overview — Golf Statistics ETL + Analytics

## One‑line summary
A full end‑to‑end data pipeline that captures personal golf stats from Excel, loads them into PostgreSQL, transforms them with dbt, and delivers interactive analytics in Streamlit.

## Why this project exists
I wanted a realistic analytics project with a clean data model, repeatable ETL, and a dashboard that answers real performance questions. Golf provides structured events (rounds and holes) with rich metrics, making it a perfect domain for analytics.

## Tech stack (100% free)
- PostgreSQL: relational database for raw and modeled data
- dbt-core: transformations, documentation, and testing
- Python (pandas, psycopg): ETL from Excel into PostgreSQL
- Streamlit + Plotly: interactive dashboard and data-entry mini app

## Data flow (end-to-end)
1. Track stats during a round in Excel
2. Python ETL validates and loads data into PostgreSQL
3. dbt models clean and structure the data for analytics
4. Streamlit dashboard visualizes KPIs and trends
5. Streamlit mini form inserts new courses, tee sets, and hole yardages

## Highlights and resume value
- Star schema design for golf analytics (courses, tees, holes, rounds, and hole-level facts)
- Data validation and cleaning in the ETL layer
- dbt models with tests and documentation
- KPI dashboard for scoring, accuracy, and trend analysis

## Example questions the dashboard answers
- Scoring trends by course and tee
- Average putts per hole and per round
- Fairway hit percentage and miss direction
- GIR (greens in regulation) rate and impact on scoring
 - Average strokes by hole number across all rounds

## What I’d add next
- Automated ingestion from Google Sheets
- Weather data enrichment by round date and location
- Shot‑level tracking (if using a GPS device)
