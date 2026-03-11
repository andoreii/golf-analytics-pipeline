select
  course_name
from {{ ref('stg_courses') }}
group by course_name
having count(*) > 1
