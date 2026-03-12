select
  round_id,
  hole_number
from {{ ref('stg_hole_stats') }}
group by round_id, hole_number
having count(*) > 1
