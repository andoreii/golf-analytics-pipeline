# Excel Template

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
- `tee_shot` (Fairway, Left, Right, Short, Long, Out Left/Right/Short/Long, Bunker Left/Right/Short/Long, Green)
- `approach` (Green, Left, Right, Short, Long, Out Left/Right/Short/Long, Bunker Left/Right/Short/Long, N/A)
- `tee_club`
- `approach_club`
- `bunker_found`
- `out_of_bounds_count`

## One file per round
Save each round as its own Excel file in `data/raw/` using the same two sheets.

Suggested naming:
- `YYYY-MM-DD_course.xlsx` (example: `2026-02-08_pine_valley.xlsx`)

## How to generate the template
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

---

# Course Import Template

Use this if you want to import a full course setup (course + tees + holes + yardages) from one Excel file.

## Sheets

### 1) course (single row)
- `course_name`
- `location`
- `notes`

### 2) tees
- `tee_name`
- `course_rating`
- `slope_rating`
- `yardage_total`

### 3) holes
- `hole_number`
- `par`

### 4) tee_holes
- `tee_name`
- `hole_number`
- `yardage`

## Generate the template
Run:
```
python scripts/create_course_import_template.py
```
This creates:
- `templates/course_import_template.xlsx`

## Import the course
Save each course as its own file in `data/raw/` using this pattern:
- `course_<short_name>.xlsx` (example: `course_pine_valley.xlsx`)

Then run:
```
python scripts/import_course_excel.py
```
