with testraw as (
    
    select
    input,
    expected_output,
    input:col1 as expr,
    input:col2 as delim
   
from {{ ref('springbrickstests')}}
where function_name = 'strtok_to_array'
),

test as (
select input,
expected_output,
{{strtok_to_array('expr', 'delim')}} as actual_output
from testraw

)

select *
from test
where expected_output <> actual_output::string
