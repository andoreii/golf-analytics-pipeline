select
  r.round_id,
  r.round_external_id,
  r.date_played,
  r.holes_played,
  r.conditions,
  r.round_type,
  r.round_format,
  r.notes,
  c.course_id,
  c.course_name,
  t.tee_id,
  t.tee_name,
  t.course_rating,
  t.slope_rating,
  t.yardage as tee_yardage
from {{ ref('stg_rounds') }} r
join {{ ref('stg_courses') }} c on r.course_id = c.course_id
left join {{ ref('stg_tees') }} t on r.tee_id = t.tee_id
