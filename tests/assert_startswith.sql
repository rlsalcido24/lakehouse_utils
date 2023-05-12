select
    {{startswith(input,'te')}} as output
from {{ ref('springbricks_tests')}}
where function_name = 'startswith'
    and expected_output <> output
