-- Enforce stable business keys used by ETL and the UI.

CREATE UNIQUE INDEX IF NOT EXISTS idx_courses_course_name_unique
  ON courses(course_name);

CREATE UNIQUE INDEX IF NOT EXISTS idx_tees_course_tee_name_unique
  ON tees(course_id, tee_name);
