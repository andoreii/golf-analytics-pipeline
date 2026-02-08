"""Load round + hole stats from Excel files into PostgreSQL."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

import pandas as pd
import psycopg
from dotenv import load_dotenv

ALLOWED_HOLES_PLAYED = {"Front 9", "Back 9", "18"}
ALLOWED_ROUND_TYPE = {"Practice", "Tournament", "Casual"}
ALLOWED_ROUND_FORMAT = {"Stroke", "Match", "Scramble", "Other"}
ALLOWED_TEE_SHOT = {"Fairway", "Left", "Right", "Short", "Long"}
ALLOWED_APPROACH = {"Green", "Left", "Right", "Short", "Long"}

REQUIRED_ROUNDS_COLS = {
    "round_external_id",
    "date_played",
    "course_name",
    "tee_name",
    "holes_played",
    "round_type",
    "round_format",
}

REQUIRED_HOLE_COLS = {
    "round_external_id",
    "hole_number",
    "strokes",
    "putts",
}


def get_conn() -> psycopg.Connection:
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "golf_stats"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


def ensure_columns(df: pd.DataFrame, required: Iterable[str], label: str) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"{label} sheet missing columns: {missing}")


def validate_rounds(rounds_df: pd.DataFrame) -> None:
    ensure_columns(rounds_df, REQUIRED_ROUNDS_COLS, "rounds")
    if len(rounds_df) != 1:
        raise ValueError("rounds sheet must contain exactly 1 row per file.")

    row = rounds_df.iloc[0]
    if row["holes_played"] not in ALLOWED_HOLES_PLAYED:
        raise ValueError("Invalid holes_played value.")
    if row["round_type"] not in ALLOWED_ROUND_TYPE:
        raise ValueError("Invalid round_type value.")
    if row["round_format"] not in ALLOWED_ROUND_FORMAT:
        raise ValueError("Invalid round_format value.")


def validate_holes(holes_df: pd.DataFrame) -> None:
    ensure_columns(holes_df, REQUIRED_HOLE_COLS, "hole_stats")
    if holes_df["hole_number"].isna().any():
        raise ValueError("hole_stats: hole_number cannot be empty.")
    if holes_df["strokes"].isna().any():
        raise ValueError("hole_stats: strokes cannot be empty.")
    if holes_df["putts"].isna().any():
        raise ValueError("hole_stats: putts cannot be empty.")

    if "tee_shot" in holes_df.columns:
        invalid = holes_df["tee_shot"].dropna().isin(ALLOWED_TEE_SHOT)
        if not invalid.all():
            raise ValueError("hole_stats: invalid tee_shot value.")
    if "approach" in holes_df.columns:
        invalid = holes_df["approach"].dropna().isin(ALLOWED_APPROACH)
        if not invalid.all():
            raise ValueError("hole_stats: invalid approach value.")


def main() -> None:
    load_dotenv()

    input_dir = Path("data/raw")
    files = sorted(input_dir.glob("*.xlsx"))
    if not files:
        raise FileNotFoundError("No Excel files found in data/raw/.")

    with get_conn() as conn:
        for path in files:
            print(f"Processing {path.name}...")
            rounds_df = pd.read_excel(path, sheet_name="rounds")
            holes_df = pd.read_excel(path, sheet_name="hole_stats")

            validate_rounds(rounds_df)
            validate_holes(holes_df)

            round_row = rounds_df.iloc[0]
            round_external_id = str(round_row["round_external_id"]).strip()

            with conn.cursor() as cur:
                # Find course and tee
                cur.execute(
                    "SELECT course_id FROM courses WHERE course_name = %s",
                    (round_row["course_name"],),
                )
                course = cur.fetchone()
                if not course:
                    raise ValueError(
                        f"Course not found: {round_row['course_name']}"
                    )
                course_id = course[0]

                cur.execute(
                    """
                    SELECT tee_id FROM tees
                    WHERE course_id = %s AND tee_name = %s
                    """,
                    (course_id, round_row["tee_name"]),
                )
                tee = cur.fetchone()
                if not tee:
                    raise ValueError(
                        f"Tee not found: {round_row['tee_name']} "
                        f"for course {round_row['course_name']}"
                    )
                tee_id = tee[0]

                # Insert round if not already present
                cur.execute(
                    "SELECT round_id FROM rounds WHERE round_external_id = %s",
                    (round_external_id,),
                )
                existing = cur.fetchone()
                if existing:
                    print(f"Round {round_external_id} already exists. Skipping.")
                    conn.rollback()
                    continue

                cur.execute(
                    """
                    INSERT INTO rounds (
                        course_id, tee_id, date_played, holes_played,
                        conditions, round_type, round_format, notes,
                        round_external_id
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING round_id
                    """,
                    (
                        course_id,
                        tee_id,
                        round_row["date_played"],
                        round_row["holes_played"],
                        round_row.get("conditions"),
                        round_row["round_type"],
                        round_row["round_format"],
                        round_row.get("notes"),
                        round_external_id,
                    ),
                )
                round_id = cur.fetchone()[0]

                for _, row in holes_df.iterrows():
                    cur.execute(
                        """
                        INSERT INTO hole_stats (
                            round_id, hole_number, strokes, putts,
                            tee_shot, approach, tee_club, approach_club,
                            bunker_found
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                        ),
                    )

                conn.commit()
                print(f"Inserted round {round_external_id} with {len(holes_df)} holes.")


if __name__ == "__main__":
    main()
