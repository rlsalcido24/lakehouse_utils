with test as (
    
    select
    'abcd1234' as inputuno,
    '2882343476' as snowoutputuno,
    {{strtol('inputuno', 16)}} as dbxoutputuno,
    '1234567' as inputdos,
    '342391' as snowoutputdos,
    {{strtol('inputdos', 8)}} as dbxoutputdos,
    '110101' as inputtres,
    '53' as snowoutputtres,
    {{strtol('inputtres', 2)}} as dbxoutputtres


)

select *
from test
where (snowoutputuno <> dbxoutputuno
	or snowoutputdos <> dbxoutputdos 
	or snowoutputtres <> dbxoutputtres)