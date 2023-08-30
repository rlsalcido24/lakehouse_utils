with test as (
    
    select
    input,
    expected_output,
    {{contains('input','"te"')}} as actual_output
from {{ ref('springbrickstests')}}
where function_name = 'contains'
)

select *
from test
where expected_output::boolean <> actual_output
