with testraw as (
    
    select
    input,
    expected_output
   
from {{ ref('springbrickstests')}}
where function_name = 'json_extract_path_text'
),

test as (
select input,
expected_output,
{{json_extract_path_text('input','col1')}} as actual_output
from testraw

)

select *
from test
where expected_output <> actual_output
