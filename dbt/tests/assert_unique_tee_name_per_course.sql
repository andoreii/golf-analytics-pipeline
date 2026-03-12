select
  course_id,
  tee_name
from {{ ref('stg_tees') }}
group by course_id, tee_name
having count(*) > 1
