-- Keep round context in conditions and remove redundant weather field.

ALTER TABLE rounds
DROP COLUMN IF EXISTS weather;
