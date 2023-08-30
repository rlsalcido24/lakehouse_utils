with test as (
    
    select
    input,
    expected_output,
    {{startswith('input','"te"')}} as actual_output
from {{ ref('springbrickstests')}}
where function_name = 'startswith'
     
)

select *
from test
where expected_output::boolean <> actual_output
