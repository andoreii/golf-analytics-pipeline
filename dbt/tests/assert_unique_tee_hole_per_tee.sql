select
  tee_id,
  hole_number
from {{ ref('stg_tee_holes') }}
group by tee_id, hole_number
having count(*) > 1
