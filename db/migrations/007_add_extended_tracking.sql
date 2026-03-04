-- Add expanded round context and hole-level tracking fields.

ALTER TABLE holes
ADD COLUMN IF NOT EXISTS hole_handicap_index INT;

ALTER TABLE holes
DROP CONSTRAINT IF EXISTS holes_hole_handicap_index_check;

ALTER TABLE holes
ADD CONSTRAINT holes_hole_handicap_index_check
CHECK (
  hole_handicap_index IS NULL
  OR hole_handicap_index BETWEEN 1 AND 18
);

ALTER TABLE rounds
ADD COLUMN IF NOT EXISTS weather TEXT,
ADD COLUMN IF NOT EXISTS walking_vs_riding TEXT,
ADD COLUMN IF NOT EXISTS time_of_day TEXT,
ADD COLUMN IF NOT EXISTS mental_state INT;

ALTER TABLE rounds
DROP CONSTRAINT IF EXISTS rounds_walking_vs_riding_check;

ALTER TABLE rounds
ADD CONSTRAINT rounds_walking_vs_riding_check
CHECK (
  walking_vs_riding IS NULL
  OR walking_vs_riding IN ('Walking', 'Riding', 'Push Cart', 'Mixed')
);

ALTER TABLE rounds
DROP CONSTRAINT IF EXISTS rounds_time_of_day_check;

ALTER TABLE rounds
ADD CONSTRAINT rounds_time_of_day_check
CHECK (
  time_of_day IS NULL
  OR time_of_day IN ('Early Morning', 'Morning', 'Afternoon', 'Evening', 'Twilight')
);

ALTER TABLE rounds
DROP CONSTRAINT IF EXISTS rounds_mental_state_check;

ALTER TABLE rounds
ADD CONSTRAINT rounds_mental_state_check
CHECK (
  mental_state IS NULL
  OR mental_state BETWEEN 1 AND 5
);

ALTER TABLE hole_stats
ADD COLUMN IF NOT EXISTS penalty_strokes INT NOT NULL DEFAULT 0,
ADD COLUMN IF NOT EXISTS up_and_down_success BOOLEAN,
ADD COLUMN IF NOT EXISTS sand_save_success BOOLEAN,
ADD COLUMN IF NOT EXISTS three_putt BOOLEAN,
ADD COLUMN IF NOT EXISTS gir_opportunity BOOLEAN,
ADD COLUMN IF NOT EXISTS fairway_opportunity BOOLEAN,
ADD COLUMN IF NOT EXISTS hazard_count INT NOT NULL DEFAULT 0;

ALTER TABLE hole_stats
DROP CONSTRAINT IF EXISTS hole_stats_penalty_strokes_check;

ALTER TABLE hole_stats
ADD CONSTRAINT hole_stats_penalty_strokes_check
CHECK (penalty_strokes BETWEEN 0 AND 10);

ALTER TABLE hole_stats
DROP CONSTRAINT IF EXISTS hole_stats_hazard_count_check;

ALTER TABLE hole_stats
ADD CONSTRAINT hole_stats_hazard_count_check
CHECK (hazard_count BETWEEN 0 AND 10);

COMMENT ON COLUMN holes.hole_handicap_index IS 'Stroke index / handicap ranking for the hole (1-18).';
COMMENT ON COLUMN rounds.weather IS 'Weather summary for the round.';
COMMENT ON COLUMN rounds.walking_vs_riding IS 'Whether the round was walked, ridden, or mixed.';
COMMENT ON COLUMN rounds.time_of_day IS 'General tee-time bucket for the round.';
COMMENT ON COLUMN rounds.mental_state IS 'Self-rating of mental state on a 1-5 scale.';
COMMENT ON COLUMN hole_stats.penalty_strokes IS 'Penalty strokes taken on the hole.';
COMMENT ON COLUMN hole_stats.up_and_down_success IS 'Whether par was saved after missing GIR.';
COMMENT ON COLUMN hole_stats.sand_save_success IS 'Whether par was saved after a greenside bunker.';
COMMENT ON COLUMN hole_stats.three_putt IS 'Whether the hole included a three-putt or worse.';
COMMENT ON COLUMN hole_stats.gir_opportunity IS 'Whether the hole should count as a GIR opportunity.';
COMMENT ON COLUMN hole_stats.fairway_opportunity IS 'Whether the hole should count as a fairway opportunity.';
COMMENT ON COLUMN hole_stats.hazard_count IS 'Number of hazards found on the hole.';
