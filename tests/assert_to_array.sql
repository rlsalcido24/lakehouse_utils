with test as (
    
    select
    input,
    split(input, ",")::array<int> as expected_output
    ,{{to_array('input')}} as actual_output
from {{ ref('springbrickstests')}}
where function_name = 'to_array'
)

select *
from test
where expected_output <> actual_output
