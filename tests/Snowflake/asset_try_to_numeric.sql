with test as (
    
    select
    '345.123' as inputuno,
    '345' as snowoutputuno,
    {{try_to_numeric('inputuno')}} as dbxoutputuno,
    '345.12' as snowoutputunoa,
    'NULL' as snowoutputunob,
    {{try_to_numeric('inputuno', 10, 2)}} as dbxoutputunoa ,
    {{try_to_numeric('inputuno', 4, 2)}} as dbxoutputunob ,
    '$345.12' as inputdos,
    '345.12' as snowoutputdos,
    'NULL' as snowoutputdosb,
    {{try_to_numeric('inputdos', "$999.00")}} as dbxoutputdos,
    {{try_to_numeric('inputdos', 5, 2)}} as dbxoutputdosb



)

select *
from test
where (snowoutputuno <> dbxoutputuno or snowoutputunoa <> dbxoutputunoa
	or snowoutputdos <> dbxoutputdos)
