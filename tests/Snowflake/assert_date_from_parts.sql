with testraw as (
    
    select
    input,
    expected_output,
    input:col1 as year,
    input:col2 as month,
    input:col3 as day,
    to_date(expected_output,'d/M/yyyy[ H:m]') as expected_output_formatted
   
from {{ ref('springbrickstests')}}
where function_name = 'date_from_parts'
),

test as (
select input,
expected_output_formatted,
{{date_from_parts('year','month','day')}} as actual_output
from testraw

)

select *
from test
where expected_output_formatted <> actual_output
