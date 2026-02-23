-- Expand allowed values for tee_shot and approach.

ALTER TABLE hole_stats
DROP CONSTRAINT IF EXISTS hole_stats_tee_shot_check;

ALTER TABLE hole_stats
DROP CONSTRAINT IF EXISTS hole_stats_approach_check;

ALTER TABLE hole_stats
DROP CONSTRAINT IF EXISTS hole_stats_tee_shot_allowed_check;

ALTER TABLE hole_stats
DROP CONSTRAINT IF EXISTS hole_stats_approach_allowed_check;

ALTER TABLE hole_stats
ADD CONSTRAINT hole_stats_tee_shot_allowed_check
CHECK (
  tee_shot IS NULL OR tee_shot IN (
    'Fairway', 'Left', 'Right', 'Short', 'Long',
    'Out Left', 'Out Right', 'Out Short', 'Out Long',
    'Bunker Left', 'Bunker Right', 'Bunker Short', 'Bunker Long',
    'Green'
  )
);

ALTER TABLE hole_stats
ADD CONSTRAINT hole_stats_approach_allowed_check
CHECK (
  approach IS NULL OR approach IN (
    'Green', 'Left', 'Right', 'Short', 'Long',
    'Out Left', 'Out Right', 'Out Short', 'Out Long',
    'Bunker Left', 'Bunker Right', 'Bunker Short', 'Bunker Long',
    'N/A'
  )
);
