-- Track out-of-bounds balls per hole

ALTER TABLE hole_stats
ADD COLUMN IF NOT EXISTS out_of_bounds_count INT NOT NULL DEFAULT 0;

ALTER TABLE hole_stats
ADD CONSTRAINT hole_stats_out_of_bounds_count_check
CHECK (out_of_bounds_count BETWEEN 0 AND 5);

COMMENT ON COLUMN hole_stats.out_of_bounds_count IS 'Number of out-of-bounds balls on the hole.';
