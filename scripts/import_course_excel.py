"""Import course(s) (with tees, holes, and yardages) from Excel."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv

REQUIRED_SHEETS = {"course", "tees", "holes", "tee_holes"}


def get_conn() -> psycopg.Connection:
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "golf_stats"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


def main() -> None:
    load_dotenv()

    input_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(input_dir.glob("course_*.xlsx"))
    if not files:
        raise FileNotFoundError("No course files found. Expected data/raw/course_*.xlsx")

    with get_conn() as conn:
        for input_path in files:
            xls = pd.ExcelFile(input_path)
            if not REQUIRED_SHEETS.issubset(set(xls.sheet_names)):
                missing = REQUIRED_SHEETS - set(xls.sheet_names)
                raise ValueError(f"{input_path.name} missing sheets: {sorted(missing)}")

            course_df = pd.read_excel(xls, sheet_name="course")
            tees_df = pd.read_excel(xls, sheet_name="tees")
            holes_df = pd.read_excel(xls, sheet_name="holes")
            tee_holes_df = pd.read_excel(xls, sheet_name="tee_holes")

            if len(course_df) != 1:
                raise ValueError(f"{input_path.name}: course sheet must have exactly one row")

            course_row = course_df.iloc[0]
            course_name = str(course_row["course_name"]).strip()
            if not course_name:
                raise ValueError(f"{input_path.name}: course_name is required")

            with conn.cursor() as cur:
                cur.execute(
                    "select course_id from courses where course_name = %s",
                    (course_name,),
                )
                if cur.fetchone():
                    print(f"{input_path.name}: course already exists, skipping.")
                    conn.rollback()
                    input_path.rename(processed_dir / input_path.name)
                    continue

                cur.execute(
                    """
                    insert into courses (course_name, location, notes)
                    values (%s, %s, %s)
                    returning course_id
                    """,
                    (
                        course_name,
                        str(course_row.get("location") or "").strip() or None,
                        str(course_row.get("notes") or "").strip() or None,
                    ),
                )
                course_id = cur.fetchone()[0]

                tee_id_map = {}
                for _, row in tees_df.iterrows():
                    tee_name = str(row.get("tee_name") or "").strip()
                    if not tee_name:
                        raise ValueError(f"{input_path.name}: tee_name cannot be empty")
                    cur.execute(
                        """
                        insert into tees (course_id, tee_name, course_rating, slope_rating, yardage)
                        values (%s, %s, %s, %s, %s)
                        returning tee_id
                        """,
                        (
                            course_id,
                            tee_name,
                            row.get("course_rating"),
                            row.get("slope_rating"),
                            row.get("yardage_total"),
                        ),
                    )
                    tee_id_map[tee_name] = cur.fetchone()[0]

                for _, row in holes_df.iterrows():
                    cur.execute(
                        """
                        insert into holes (course_id, hole_number, par)
                        values (%s, %s, %s)
                        """,
                        (course_id, int(row["hole_number"]), int(row["par"])),
                    )

                for _, row in tee_holes_df.iterrows():
                    tee_name = str(row.get("tee_name") or "").strip()
                    if tee_name not in tee_id_map:
                        raise ValueError(f"{input_path.name}: unknown tee_name {tee_name}")
                    cur.execute(
                        """
                        insert into tee_holes (tee_id, hole_number, yardage)
                        values (%s, %s, %s)
                        """,
                        (
                            tee_id_map[tee_name],
                            int(row["hole_number"]),
                            int(row["yardage"]),
                        ),
                    )

            conn.commit()
            print(f"Imported course: {course_name}")
            input_path.rename(processed_dir / input_path.name)


if __name__ == "__main__":
    main()
