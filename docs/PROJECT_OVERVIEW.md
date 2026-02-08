# Project Overview — Golf Statistics ETL + Analytics

## One‑line summary
An end‑to‑end pipeline I built for my own golf stats: Excel tracking → PostgreSQL → dbt models → Streamlit analytics.

## Why this project exists
I wanted a simple, personal system that makes me a better golfer. That meant a clean data model, repeatable ETL, and a dashboard that answers the questions I actually ask after a round.

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

## Highlights
- Clean relational model for courses, tees, holes, rounds, and hole stats
- ETL with validation so bad data doesn’t sneak in
- dbt models for consistent metrics
- Dashboard for scoring, accuracy, and trend analysis

## Example analytics
- Scoring trends by course and tee
- Average putts per hole and per round
- Fairway hit percentage and miss direction
- GIR (greens in regulation) rate and impact on scoring
 - Average strokes by hole number across all rounds

## add next
- Optional Google Sheets ingestion
- Weather enrichment by round date and location
- Shot‑level tracking from a GPS device
