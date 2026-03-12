select
  course_id,
  hole_number
from {{ ref('stg_holes') }}
group by course_id, hole_number
having count(*) > 1
