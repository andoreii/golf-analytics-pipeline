-- Track greens in regulation explicitly instead of inferring from approach result.

ALTER TABLE hole_stats
ADD COLUMN IF NOT EXISTS green_in_reg BOOLEAN;

COMMENT ON COLUMN hole_stats.green_in_reg IS 'Whether the green was reached in regulation on the hole.';
