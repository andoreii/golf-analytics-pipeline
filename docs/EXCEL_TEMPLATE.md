# Excel Template (User-Friendly, Minimal)

The template uses two sheets:

## 1) rounds
One row per round.

Columns:
- `round_external_id` (unique ID you control, e.g., `2026-02-08-PineValley`)
- `date_played` (YYYY-MM-DD)
- `course_name` (must match an existing course in the database)
- `tee_name` (must match a tee for that course)
- `holes_played` (Front 9, Back 9, 18)
- `conditions` (free text)
- `round_type` (Practice, Tournament, Casual)
- `round_format` (Stroke, Match, Scramble, Other)
- `notes`

## 2) hole_stats
One row per hole played.

Columns:
- `round_external_id` (links to the round)
- `hole_number` (1-18)
- `strokes`
- `putts`
- `tee_shot` (Fairway, Left, Right, Short, Long)
- `approach` (Green, Left, Right, Short, Long)
- `tee_club`
- `approach_club`
- `bunker_found`

## One file per round
Save each round as its own Excel file in `data/raw/` using the same two sheets.\n\nSuggested naming:\n- `YYYY-MM-DD_course.xlsx` (example: `2026-02-08_pine_valley.xlsx`)\n\n## How to generate the template
Run:
```
python scripts/create_excel_template.py
```
This creates:
- `templates/golf_stats_template.xlsx`

The template includes:
- frozen header row
- dropdown lists for allowed values
- clean column widths
- a single example row per sheet
