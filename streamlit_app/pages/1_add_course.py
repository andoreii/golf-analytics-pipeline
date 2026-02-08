"""Mini Streamlit form to add a course, tees, and hole pars/yardages."""

from __future__ import annotations

import os
from typing import List

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


st.set_page_config(page_title="Add Course", layout="wide")

st.title("Add a New Course")
st.caption("Add course info, tee sets, hole pars, and per-tee yardages.")

with st.form("course_form"):
    col1, col2 = st.columns(2)
    with col1:
        course_name = st.text_input("Course name", placeholder="Pine Valley Golf Club")
        location = st.text_input("Location", placeholder="Pine Valley, NJ")
    with col2:
        notes = st.text_area("Notes", placeholder="Any notes about the course")

    st.subheader("Tee Sets")
    tee_count = st.number_input("Number of tee sets", min_value=1, max_value=6, value=3)

    tee_rows = pd.DataFrame(
        {
            "tee_name": ["Blue", "White", "Red"][:tee_count] + [""] * max(0, tee_count - 3),
            "course_rating": [71.2, 69.5, 67.8][:tee_count] + [None] * max(0, tee_count - 3),
            "slope_rating": [128, 122, 115][:tee_count] + [None] * max(0, tee_count - 3),
            "yardage_total": [6900, 6400, 5900][:tee_count] + [None] * max(0, tee_count - 3),
        }
    )

    tees_df = st.data_editor(
        tee_rows,
        num_rows="fixed",
        use_container_width=True,
        column_config={
            "tee_name": st.column_config.TextColumn("Tee name"),
            "course_rating": st.column_config.NumberColumn("Course rating"),
            "slope_rating": st.column_config.NumberColumn("Slope rating"),
            "yardage_total": st.column_config.NumberColumn("Total yardage"),
        },
    )

    st.subheader("Holes")
    st.write("Enter par and yardage for each hole. Yardage columns follow tee order.")

    hole_numbers = list(range(1, 19))
    yardage_columns = [f"tee_{i+1}_yardage" for i in range(int(tee_count))]

    hole_rows = {
        "hole_number": hole_numbers,
        "par": [4] * 18,
    }
    for col in yardage_columns:
        hole_rows[col] = [None] * 18

    holes_df = st.data_editor(
        pd.DataFrame(hole_rows),
        num_rows="fixed",
        use_container_width=True,
        column_config={
            "hole_number": st.column_config.NumberColumn("Hole"),
            "par": st.column_config.NumberColumn("Par"),
        },
    )

    submitted = st.form_submit_button("Save course")

if submitted:
    if not course_name:
        st.error("Course name is required.")
        st.stop()

    if tees_df["tee_name"].isna().any() or (tees_df["tee_name"].str.strip() == "").any():
        st.error("Every tee set must have a name.")
        st.stop()

    if holes_df["par"].isna().any():
        st.error("Each hole needs a par value.")
        st.stop()

    with get_conn() as conn:
        with conn.cursor() as cur:
            # Insert course
            cur.execute(
                """
                INSERT INTO courses (course_name, location, notes)
                VALUES (%s, %s, %s)
                RETURNING course_id
                """,
                (course_name.strip(), location.strip() or None, notes.strip() or None),
            )
            course_id = cur.fetchone()[0]

            # Insert tees
            tee_ids: List[int] = []
            for _, row in tees_df.iterrows():
                cur.execute(
                    """
                    INSERT INTO tees (course_id, tee_name, course_rating, slope_rating, yardage)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING tee_id
                    """,
                    (
                        course_id,
                        str(row["tee_name"]).strip(),
                        row.get("course_rating"),
                        row.get("slope_rating"),
                        row.get("yardage_total"),
                    ),
                )
                tee_ids.append(cur.fetchone()[0])

            # Insert holes (pars)
            for _, row in holes_df.iterrows():
                cur.execute(
                    """
                    INSERT INTO holes (course_id, hole_number, par)
                    VALUES (%s, %s, %s)
                    """,
                    (course_id, int(row["hole_number"]), int(row["par"])),
                )

            # Insert per-tee yardages
            for tee_index, tee_id in enumerate(tee_ids):
                yardage_col = f"tee_{tee_index + 1}_yardage"
                if yardage_col not in holes_df.columns:
                    continue
                for _, row in holes_df.iterrows():
                    yardage_val = row.get(yardage_col)
                    if pd.isna(yardage_val):
                        continue
                    cur.execute(
                        """
                        INSERT INTO tee_holes (tee_id, hole_number, yardage)
                        VALUES (%s, %s, %s)
                        """,
                        (tee_id, int(row["hole_number"]), int(yardage_val)),
                    )

        conn.commit()

    st.success("Course saved successfully.")
