select
  r.round_id,
  r.round_external_id,
  r.date_played,
  r.course_name,
  r.tee_name,
  count(*) as holes_tracked,
  sum(hs.strokes) as total_strokes,
  sum(hs.putts) as total_putts,
  avg(hs.putts::numeric) as avg_putts_per_hole,
  sum(case when hs.tee_shot = 'Fairway' then 1 else 0 end) as fairways_hit,
  sum(case when hs.approach = 'Green' then 1 else 0 end) as greens_in_reg
from {{ ref('fact_rounds') }} r
join {{ ref('fact_hole_stats') }} hs on r.round_id = hs.round_id
group by 1,2,3,4,5
