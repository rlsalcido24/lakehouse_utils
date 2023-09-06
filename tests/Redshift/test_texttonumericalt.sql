with test as (
    
    select
    '1.5' as inputuno,
    '2' as snowoutputuno,
    {{texttonumericalt('inputuno')}} as dbxoutputuno,
    '2.51' as inputdos,
    '3' as snowoutputdos,
    {{texttonumericalt('inputdos')}} as dbxoutputdos,
    '123.52501' as inputtres,
    '123.53' as snowoutputtres,
    {{texttonumericalt('inputtres', 10, 2)}} as dbxoutputtres


)

select *
from test
where (snowoutputuno <> dbxoutputuno
	or snowoutputdos <> dbxoutputdos 
	or snowoutputtres <> dbxoutputtres)
