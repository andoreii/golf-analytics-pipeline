-- Add external round identifier for ETL linkage

ALTER TABLE rounds
ADD COLUMN IF NOT EXISTS round_external_id TEXT;

COMMENT ON COLUMN rounds.round_external_id IS 'Unique ID from Excel to link round + hole stats.';

CREATE UNIQUE INDEX IF NOT EXISTS idx_rounds_external_id
  ON rounds(round_external_id)
  WHERE round_external_id IS NOT NULL;
