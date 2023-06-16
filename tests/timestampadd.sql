with testraw as (
    
    select
    input,
    expected_output,
    input:col1 as unit,
    input:col2 as measure,
    input:col3 as base
   
from {{ ref('springbrickstests')}}
where function_name = 'timestampadd'
),

test as (
select input,
expected_output,
{{timestampadd('unit', 'measure', 'base')}} as actual_output,
concat('"',actual_output, '"') as actual_output_quotes
from testraw

)

select *
from test
where expected_output <> actual_output_quotes
