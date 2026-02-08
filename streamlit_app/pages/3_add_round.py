"""Mini Streamlit form to add a round and hole stats."""

from __future__ import annotations

import os
from datetime import date

import pandas as pd
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


def fetch_courses(conn: psycopg.Connection) -> pd.DataFrame:
    return pd.read_sql(
        "select course_id, course_name from courses order by course_name", conn
    )


def fetch_tees(conn: psycopg.Connection, course_id: int) -> pd.DataFrame:
    return pd.read_sql(
        """
        select tee_id, tee_name
        from tees
        where course_id = %s
        order by tee_name
        """,
        conn,
        params=(course_id,),
    )


st.set_page_config(page_title="Add Round", layout="wide")

st.title("Add a Round")
st.caption("Enter round details and hole-by-hole stats.")

with get_conn() as conn:
    courses_df = fetch_courses(conn)

if courses_df.empty:
    st.warning("Add a course first before entering rounds.")
    st.stop()

course_name = st.selectbox("Course", courses_df["course_name"].tolist())
course_id = int(courses_df.loc[courses_df["course_name"] == course_name, "course_id"].iloc[0])

with get_conn() as conn:
    tees_df = fetch_tees(conn, course_id)

if tees_df.empty:
    st.warning("Add tee sets for this course before entering rounds.")
    st.stop()

tee_name = st.selectbox("Tee", tees_df["tee_name"].tolist())
tee_id = int(tees_df.loc[tees_df["tee_name"] == tee_name, "tee_id"].iloc[0])

col1, col2, col3 = st.columns(3)
with col1:
    date_played = st.date_input("Date played", value=date.today())
with col2:
    holes_played = st.selectbox("Holes played", ["18", "Front 9", "Back 9"])
with col3:
    round_type = st.selectbox("Round type", ["Practice", "Tournament", "Casual"])

col4, col5 = st.columns(2)
with col4:
    round_format = st.selectbox("Round format", ["Stroke", "Match", "Scramble", "Other"])
with col5:
    conditions = st.text_input("Conditions", placeholder="Sunny, light wind")

round_external_id = st.text_input(
    "Round external ID",
    placeholder="2026-02-08-PineValley",
)
notes = st.text_area("Notes", placeholder="Short notes about the round")

if holes_played == "18":
    hole_numbers = list(range(1, 19))
elif holes_played == "Front 9":
    hole_numbers = list(range(1, 10))
else:
    hole_numbers = list(range(10, 19))

hole_rows = {
    "hole_number": hole_numbers,
    "strokes": [None] * len(hole_numbers),
    "putts": [None] * len(hole_numbers),
    "tee_shot": [None] * len(hole_numbers),
    "approach": [None] * len(hole_numbers),
    "tee_club": [None] * len(hole_numbers),
    "approach_club": [None] * len(hole_numbers),
    "bunker_found": [0] * len(hole_numbers),
    "out_of_bounds_count": [0] * len(hole_numbers),
}

st.subheader("Hole Stats")
holes_df = st.data_editor(
    pd.DataFrame(hole_rows),
    num_rows="fixed",
    use_container_width=True,
    column_config={
        "hole_number": st.column_config.NumberColumn("Hole", disabled=True),
        "strokes": st.column_config.NumberColumn("Strokes"),
        "putts": st.column_config.NumberColumn("Putts"),
        "tee_shot": st.column_config.SelectboxColumn(
            "Tee Shot",
            options=["Fairway", "Left", "Right", "Short", "Long"],
        ),
        "approach": st.column_config.SelectboxColumn(
            "Approach",
            options=["Green", "Left", "Right", "Short", "Long"],
        ),
        "out_of_bounds_count": st.column_config.NumberColumn("OB"),
    },
)

save_round = st.button("Save round")

if save_round:
    if not round_external_id.strip():
        st.error("Round external ID is required.")
        st.stop()

    if holes_df["strokes"].isna().any() or holes_df["putts"].isna().any():
        st.error("Please fill strokes and putts for each hole.")
        st.stop()

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "select 1 from rounds where round_external_id = %s",
                (round_external_id.strip(),),
            )
            if cur.fetchone():
                st.error("That round_external_id already exists.")
                st.stop()

            cur.execute(
                """
                insert into rounds (
                    course_id, tee_id, date_played, holes_played,
                    conditions, round_type, round_format, notes,
                    round_external_id
                )
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                returning round_id
                """,
                (
                    course_id,
                    tee_id,
                    date_played,
                    holes_played,
                    conditions.strip() or None,
                    round_type,
                    round_format,
                    notes.strip() or None,
                    round_external_id.strip(),
                ),
            )
            round_id = cur.fetchone()[0]

            for _, row in holes_df.iterrows():
                cur.execute(
                    """
                    insert into hole_stats (
                        round_id, hole_number, strokes, putts,
                        tee_shot, approach, tee_club, approach_club,
                        bunker_found, out_of_bounds_count
                    )
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        round_id,
                        int(row["hole_number"]),
                        int(row["strokes"]),
                        int(row["putts"]),
                        row.get("tee_shot"),
                        row.get("approach"),
                        row.get("tee_club"),
                        row.get("approach_club"),
                        int(row.get("bunker_found") or 0),
                        int(row.get("out_of_bounds_count") or 0),
                    ),
                )

        conn.commit()

    st.success("Round saved successfully.")
