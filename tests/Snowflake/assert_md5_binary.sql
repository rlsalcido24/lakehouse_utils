with test as (
    
    select
    input,
    expected_output,
    {{md5_binary('input')}} as actual_output
from {{ ref('springbrickstests')}}
where function_name = 'md5_binary'
)

select *
from test
where expected_output <> upper(actual_output)
