-- Per-tee hole yardages

CREATE TABLE IF NOT EXISTS tee_holes (
  tee_hole_id SERIAL PRIMARY KEY,
  tee_id      INT NOT NULL REFERENCES tees(tee_id) ON DELETE CASCADE,
  hole_number INT NOT NULL CHECK (hole_number BETWEEN 1 AND 18),
  yardage     INT NOT NULL CHECK (yardage BETWEEN 50 AND 800)
);

COMMENT ON TABLE tee_holes IS 'Per-tee yardage for each hole.';
COMMENT ON COLUMN tee_holes.hole_number IS 'Hole number (1-18).';
COMMENT ON COLUMN tee_holes.yardage IS 'Yardage for this tee on this hole.';

CREATE UNIQUE INDEX IF NOT EXISTS idx_tee_holes_tee_hole
  ON tee_holes(tee_id, hole_number);
