with testraw as (
    
    select
    input,
    expected_output,
    NULL as left,
    NULL as right
   
from {{ ref('springbrickstests')}}
where function_name = 'equal_null'
),

test as (
select input,
expected_output,
{{equal_null('left', 'right')}} as actual_output
from testraw

)

select *
from test
where expected_output::boolean <> actual_output
