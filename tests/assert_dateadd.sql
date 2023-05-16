with testraw as (
    
    select
    input,
    expected_output,
    input:col1 as unit,
    input:col2 as measure,
    input:col3 as base,
    to_date(expected_output,'d/M/yyyy[ H:m]') as expected_output_formatted
   
from {{ ref('springbrickstests')}}
where function_name = 'dateadd'
),

test as (
select input,
expected_output_formatted, base,
{{dateadd('unit','measure','base')}} as actual_output
from testraw

)


select *
from test
--where expected_output_formatted <> actual_output
