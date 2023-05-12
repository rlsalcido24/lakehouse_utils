with test as (
    
    select
    *
    ,{{contains('input','"te"')}} as actual_output
from {{ ref('springbrickstests')}}
where function_name = 'contains'
)

select *
from test
where expected_output <> actual_output
