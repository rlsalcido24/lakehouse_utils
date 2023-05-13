with test as (
    
    select
    input,
    expected_output,
    {{monthname('input')}} as actual_output
from {{ ref('springbrickstests')}}
where function_name = 'monthname'
)

select *
from test
where expected_output <> actual_output
