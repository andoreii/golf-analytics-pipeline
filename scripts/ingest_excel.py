"""Load round + hole stats from an Excel file into PostgreSQL.

Planned behavior:
- Read Excel from data/raw/
- Validate required columns
- Insert into rounds and hole_stats
- Log row counts and any validation errors
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()

    # Placeholder path for first run
    input_path = Path("data/raw/rounds.xlsx")
    if not input_path.exists():
        raise FileNotFoundError(
            "Expected Excel file at data/raw/rounds.xlsx."
        )

    # TODO: implement ETL logic
    df = pd.read_excel(input_path)
    print(f"Loaded {len(df)} rows from {input_path}")
    print("ETL not implemented yet.")


if __name__ == "__main__":
    main()
