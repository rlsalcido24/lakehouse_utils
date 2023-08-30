with test as (
    
    select
    'Snowflake' as inputuno,
    'U25vd2ZsYWtl' as snowoutputuno,
    {{base64_encode('inputuno')}} as dbxoutputuno




)

select *
from test
where (snowoutputuno <> dbxoutputuno)
