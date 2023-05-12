select
    {{to_array(input)}} as output
from {{ ref('springbricks_tests')}}
where function_name = 'to_array'
    and expected_output <> output
