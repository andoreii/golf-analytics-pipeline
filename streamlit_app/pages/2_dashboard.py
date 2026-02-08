"""Analytics dashboard for golf stats."""

from __future__ import annotations

import os

import pandas as pd
import plotly.express as px
import psycopg
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_conn() -> psycopg.Connection:
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "golf_stats"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


def load_round_kpis(conn: psycopg.Connection) -> pd.DataFrame:
    return pd.read_sql("select * from agg_round_kpis order by date_played desc", conn)


def load_hole_stats(conn: psycopg.Connection) -> pd.DataFrame:
    return pd.read_sql(
        "select * from fact_hole_stats order by date_played desc, hole_number asc",
        conn,
    )


st.set_page_config(page_title="Dashboard", layout="wide")

st.title("Golf Performance Dashboard")
st.caption("KPIs and trends from your tracked rounds.")

with get_conn() as conn:
    kpis = load_round_kpis(conn)
    holes = load_hole_stats(conn)

if kpis.empty:
    st.info("No data yet. Add a course and ingest a round to see analytics.")
    st.stop()

# Filters
kpis["date_played"] = pd.to_datetime(kpis["date_played"]).dt.date
min_date = kpis["date_played"].min()
max_date = kpis["date_played"].max()

col1, col2, col3 = st.columns(3)
with col1:
    date_range = st.date_input(
        "Date range",
        (min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
with col2:
    courses = ["All"] + sorted(kpis["course_name"].dropna().unique().tolist())
    course_choice = st.selectbox("Course", courses)
with col3:
    tees = ["All"] + sorted(kpis["tee_name"].dropna().unique().tolist())
    tee_choice = st.selectbox("Tee", tees)

start_date, end_date = date_range

filtered = kpis[
    (kpis["date_played"] >= start_date)
    & (kpis["date_played"] <= end_date)
]
if course_choice != "All":
    filtered = filtered[filtered["course_name"] == course_choice]
if tee_choice != "All":
    filtered = filtered[filtered["tee_name"] == tee_choice]

# KPI cards
c1, c2, c3, c4 = st.columns(4)

avg_score = filtered["total_strokes"].mean()
avg_putts = filtered["avg_putts_per_hole"].mean()
fairway_pct = (
    filtered["fairways_hit"].sum() / filtered["holes_tracked"].sum()
    if filtered["holes_tracked"].sum() > 0
    else 0
)
gir_pct = (
    filtered["greens_in_reg"].sum() / filtered["holes_tracked"].sum()
    if filtered["holes_tracked"].sum() > 0
    else 0
)

c1.metric("Avg Strokes", f"{avg_score:.1f}")
c2.metric("Avg Putts/Hole", f"{avg_putts:.2f}")
c3.metric("Fairway %", f"{fairway_pct:.0%}")
c4.metric("GIR %", f"{gir_pct:.0%}")

if "out_of_bounds_total" in filtered.columns:
    st.caption(f"Out-of-bounds (total): {int(filtered['out_of_bounds_total'].sum())}")

st.divider()

# Trend chart
trend = filtered.sort_values("date_played")
fig_trend = px.line(
    trend,
    x="date_played",
    y="total_strokes",
    title="Total Strokes by Round",
    markers=True,
)
st.plotly_chart(fig_trend, use_container_width=True)

# Putts distribution
fig_putts = px.histogram(
    filtered,
    x="avg_putts_per_hole",
    nbins=12,
    title="Average Putts per Hole (Distribution)",
)
st.plotly_chart(fig_putts, use_container_width=True)

st.divider()

# Hole-level breakdown
holes_filtered = holes.copy()
if course_choice != "All":
    holes_filtered = holes_filtered[holes_filtered["course_id"].isin(
        filtered["course_id"].unique()
    )]

hole_summary = (
    holes_filtered.groupby("hole_number")
    .agg(
        avg_strokes=("strokes", "mean"),
        avg_putts=("putts", "mean"),
        count=("hole_stat_id", "count"),
    )
    .reset_index()
)

fig_holes = px.bar(
    hole_summary,
    x="hole_number",
    y="avg_strokes",
    title="Average Strokes by Hole",
)
st.plotly_chart(fig_holes, use_container_width=True)

st.caption("Data source: dbt models (agg_round_kpis, fact_hole_stats)")
