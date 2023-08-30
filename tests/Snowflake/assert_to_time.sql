with testraw as (
    
    select
    input,
    expected_output,
    input:col1 as expr
   
from {{ ref('springbrickstests')}}
where function_name = 'to_time'
),

test as (
select input,
expected_output,
{{to_time('expr')}} as actual_output
from testraw

)

select *
from test
where expected_output <> actual_output
