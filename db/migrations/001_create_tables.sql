-- Golf statistics schema (PostgreSQL)
-- All columns and tables are documented with COMMENTS.

CREATE TABLE IF NOT EXISTS courses (
  course_id   SERIAL PRIMARY KEY,
  course_name TEXT NOT NULL,
  location    TEXT,
  notes       TEXT
);

COMMENT ON TABLE courses IS 'Golf courses where rounds are played.';
COMMENT ON COLUMN courses.course_name IS 'Name of the course.';
COMMENT ON COLUMN courses.location IS 'City/State or address.';
COMMENT ON COLUMN courses.notes IS 'Free-form notes about the course.';

CREATE TABLE IF NOT EXISTS tees (
  tee_id        SERIAL PRIMARY KEY,
  course_id     INT NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
  tee_name      TEXT NOT NULL,
  course_rating NUMERIC(4,1),
  slope_rating  NUMERIC(4,1),
  yardage       INT
);

COMMENT ON TABLE tees IS 'Tee sets for each course (e.g., Blue, White).';
COMMENT ON COLUMN tees.course_rating IS 'USGA course rating (example: 71.2).';
COMMENT ON COLUMN tees.slope_rating IS 'USGA slope rating (example: 128).';
COMMENT ON COLUMN tees.yardage IS 'Total yardage for 18 holes.';

CREATE TABLE IF NOT EXISTS holes (
  hole_id     SERIAL PRIMARY KEY,
  course_id   INT NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
  hole_number INT NOT NULL CHECK (hole_number BETWEEN 1 AND 18),
  par         INT NOT NULL CHECK (par BETWEEN 3 AND 5)
);

COMMENT ON TABLE holes IS 'Hole-level course definition (par for each hole).';
COMMENT ON COLUMN holes.hole_number IS 'Hole number (1-18).';
COMMENT ON COLUMN holes.par IS 'Par value (3-5).';

CREATE UNIQUE INDEX IF NOT EXISTS idx_holes_course_hole
  ON holes(course_id, hole_number);

CREATE TABLE IF NOT EXISTS rounds (
  round_id     SERIAL PRIMARY KEY,
  course_id    INT NOT NULL REFERENCES courses(course_id) ON DELETE RESTRICT,
  tee_id       INT REFERENCES tees(tee_id) ON DELETE SET NULL,
  date_played  DATE NOT NULL,
  holes_played TEXT NOT NULL CHECK (holes_played IN ('Front 9', 'Back 9', '18')),
  conditions   TEXT,
  round_type   TEXT CHECK (round_type IN ('Practice', 'Tournament', 'Casual')),
  round_format TEXT CHECK (round_format IN ('Stroke', 'Match', 'Scramble', 'Other')),
  notes        TEXT
);

COMMENT ON TABLE rounds IS 'Round-level facts for each time you play.';
COMMENT ON COLUMN rounds.holes_played IS 'Front 9, Back 9, or 18.';
COMMENT ON COLUMN rounds.round_type IS 'Type of round (Practice, Tournament, Casual).';
COMMENT ON COLUMN rounds.round_format IS 'Format (Stroke, Match, Scramble, Other).';

CREATE INDEX IF NOT EXISTS idx_rounds_date
  ON rounds(date_played);

CREATE TABLE IF NOT EXISTS hole_stats (
  hole_stat_id  SERIAL PRIMARY KEY,
  round_id      INT NOT NULL REFERENCES rounds(round_id) ON DELETE CASCADE,
  hole_number   INT NOT NULL CHECK (hole_number BETWEEN 1 AND 18),
  strokes       INT NOT NULL CHECK (strokes BETWEEN 1 AND 15),
  putts         INT NOT NULL CHECK (putts BETWEEN 0 AND 6),
  tee_shot      TEXT CHECK (
    tee_shot IN (
      'Fairway', 'Left', 'Right', 'Short', 'Long',
      'Out Left', 'Out Right', 'Out Short', 'Out Long',
      'Bunker Left', 'Bunker Right', 'Bunker Short', 'Bunker Long',
      'Green'
    )
  ),
  approach      TEXT CHECK (
    approach IN (
      'Green', 'Left', 'Right', 'Short', 'Long',
      'Out Left', 'Out Right', 'Out Short', 'Out Long',
      'Bunker Left', 'Bunker Right', 'Bunker Short', 'Bunker Long',
      'N/A'
    )
  ),
  tee_club      TEXT,
  approach_club TEXT,
  bunker_found  INT NOT NULL DEFAULT 0 CHECK (bunker_found BETWEEN 0 AND 3)
);

COMMENT ON TABLE hole_stats IS 'Hole-level performance for a specific round.';
COMMENT ON COLUMN hole_stats.tee_shot IS 'Direction/quality of the tee shot.';
COMMENT ON COLUMN hole_stats.approach IS 'Direction/quality of the approach shot.';
COMMENT ON COLUMN hole_stats.bunker_found IS 'Number of bunkers found on the hole.';

CREATE UNIQUE INDEX IF NOT EXISTS idx_hole_stats_round_hole
  ON hole_stats(round_id, hole_number);
