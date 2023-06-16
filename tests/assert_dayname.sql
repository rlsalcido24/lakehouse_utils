with testraw as (
    
    select
    input,
    expected_output,
    to_date(input,'d/M/yyyy[ H:m]') as input_formatted
   
from {{ ref('springbrickstests')}}
where function_name = 'dayname'
),

test as (
select input,
expected_output,
{{dayname('input_formatted')}} as actual_output
from testraw

)

select *
from test
where expected_output <> actual_output
