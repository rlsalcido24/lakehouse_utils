with test as (
    
    select
    *
    ,{{startswith('input','"te"')}} as actual_output
from {{ ref('springbrickstests')}}
where function_name = 'startswith'
     
)

select *
from test
where expected_output::boolean <> input
