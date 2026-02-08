"""Create a clean, user-friendly Excel template for round tracking."""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

TEMPLATE_PATH = Path("templates/golf_stats_template.xlsx")


def style_header(ws, headers: list[str]) -> None:
    header_fill = PatternFill("solid", fgColor="F2F2F2")
    header_font = Font(bold=True)
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{ws.cell(row=1, column=len(headers)).coordinate}"


def set_col_widths(ws, widths: dict[int, int]) -> None:
    for col_idx, width in widths.items():
        ws.column_dimensions[chr(64 + col_idx)].width = width


def add_validation(ws, col_letter: str, allowed: list[str]) -> None:
    formula = '"' + ",".join(allowed) + '"'
    dv = DataValidation(type="list", formula1=formula, allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"{col_letter}2:{col_letter}500")


def build_rounds_sheet(wb: Workbook) -> None:
    ws = wb.active
    ws.title = "rounds"

    headers = [
        "round_external_id",
        "date_played",
        "course_name",
        "tee_name",
        "holes_played",
        "conditions",
        "round_type",
        "round_format",
        "notes",
    ]

    style_header(ws, headers)
    set_col_widths(
        ws,
        {
            1: 18,
            2: 14,
            3: 24,
            4: 14,
            5: 14,
            6: 18,
            7: 14,
            8: 14,
            9: 28,
        },
    )

    add_validation(ws, "E", ["Front 9", "Back 9", "18"])
    add_validation(ws, "G", ["Practice", "Tournament", "Casual"])
    add_validation(ws, "H", ["Stroke", "Match", "Scramble", "Other"])

    # Example row (minimal guidance)
    ws.append(
        [
            "2026-02-08-PineValley",
            "2026-02-08",
            "Pine Valley Golf Club",
            "Blue",
            "18",
            "Sunny, light wind",
            "Practice",
            "Stroke",
            "Felt good off the tee",
        ]
    )


def build_hole_stats_sheet(wb: Workbook) -> None:
    ws = wb.create_sheet("hole_stats")

    headers = [
        "round_external_id",
        "hole_number",
        "strokes",
        "putts",
        "tee_shot",
        "approach",
        "tee_club",
        "approach_club",
        "bunker_found",
        "out_of_bounds_count",
    ]

    style_header(ws, headers)
    set_col_widths(
        ws,
        {
            1: 22,
            2: 12,
            3: 10,
            4: 10,
            5: 12,
            6: 12,
            7: 12,
            8: 14,
            9: 14,
        },
    )

    add_validation(ws, "B", [str(i) for i in range(1, 19)])
    add_validation(ws, "E", ["Fairway", "Left", "Right", "Short", "Long"])
    add_validation(ws, "F", ["Green", "Left", "Right", "Short", "Long"])

    ws.append(
        [
            "2026-02-08-PineValley",
            1,
            4,
            2,
            "Fairway",
            "Green",
            "Driver",
            "7i",
            0,
            0,
        ]
    )


def main() -> None:
    TEMPLATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    build_rounds_sheet(wb)
    build_hole_stats_sheet(wb)
    wb.save(TEMPLATE_PATH)
    print(f"Template created at {TEMPLATE_PATH}")


if __name__ == "__main__":
    main()
