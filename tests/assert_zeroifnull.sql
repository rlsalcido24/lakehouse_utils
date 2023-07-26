with test as (
    
    select
    input,
    input::decimal(9,5) as inputdec,
    expected_output,
    {{zeroifnull('inputdec')}} as actual_output
from {{ ref('springbrickstests')}}
where function_name = 'zeroifnull'
)

select *
from test
where expected_output <> actual_output
