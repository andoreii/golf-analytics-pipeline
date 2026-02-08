select
  hs.hole_stat_id,
  hs.round_id,
  r.round_external_id,
  r.date_played,
  r.course_id,
  r.tee_id,
  hs.hole_number,
  h.par,
  th.yardage,
  hs.strokes,
  hs.putts,
  hs.tee_shot,
  hs.approach,
  hs.tee_club,
  hs.approach_club,
  hs.bunker_found,
  hs.out_of_bounds_count
from {{ ref('stg_hole_stats') }} hs
join {{ ref('stg_rounds') }} r on hs.round_id = r.round_id
left join {{ ref('stg_holes') }} h
  on r.course_id = h.course_id
 and hs.hole_number = h.hole_number
left join {{ ref('stg_tee_holes') }} th
  on r.tee_id = th.tee_id
 and hs.hole_number = th.hole_number
