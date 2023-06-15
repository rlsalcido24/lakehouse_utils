with test as (
    
    select
    input,
    expected_output,
    {{week('input')}} as actual_output
from {{ ref('springbrickstests')}}
where function_name = 'week'
)

select *
from test
where expected_output <> actual_output::string
