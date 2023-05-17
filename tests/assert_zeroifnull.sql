with test as (
    
    select
    input,
    expected_output,
    {{zeroifnull('input')}} as actual_output
from {{ ref('springbrickstests')}}
where function_name = 'zeroifnull'
)

select *
from test
where expected_output <> actual_output
