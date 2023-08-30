with testraw as (
    
    select
    input,
    expected_output,
    input:col1 as unit,
    input:col2 as timeuno,
    input:col3 as timedos
   
from {{ ref('springbrickstests')}}
where function_name = 'timestampdiff'
),

test as (
select input,
expected_output,
{{timestampdiff('unit', 'timeuno', 'timedos')}} as actual_output
from testraw

)

select *
from test
where expected_output <> actual_output
