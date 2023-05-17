with test as (
    
    select
    input,
    expected_output,
    {{to_number('input')}} as actual_output
from {{ ref('springbrickstests')}}
where function_name = 'to_number_onearg'
)

select *
from test
where expected_output <> actual_output
