with test as (
    
    select
    input,
    expected_output,
    {{to_boolean('input')}} as actual_output
from {{ ref('springbrickstests')}}
where function_name = 'to_boolean'
)

select *
from test
where lower(expected_output) <> actual_output::string
