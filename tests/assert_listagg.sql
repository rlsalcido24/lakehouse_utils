with test as (
    
    select
    input,
    expected_output,
    {{listagg('input','","')}} as actual_output
from {{ ref('springbrickstests')}}
where function_name = 'listagg'
     
)

select *
from test
-- where expected_output::boolean <> actual_output
