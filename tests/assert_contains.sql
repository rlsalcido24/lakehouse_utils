select
    {{contains(input,'te')}} as output
from {{ ref('springbricks_tests')}}
where function_name = 'contains'
    and expected_output <> output
