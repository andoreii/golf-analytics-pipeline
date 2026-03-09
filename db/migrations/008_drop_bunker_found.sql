-- Remove explicit bunker counting in favor of deriving bunker-related stats
-- from tee_shot / approach outcomes.

ALTER TABLE hole_stats
DROP COLUMN IF EXISTS bunker_found;
