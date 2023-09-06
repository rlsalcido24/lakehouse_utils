with test as (
    
    select
    '5.6' as inputuno,
    '5' as snowoutputuno,
    {{convert('INT', 'inputuno')}} as dbxoutputuno,
    '5.6' as inputdos,
    '6' as snowoutputdos,
    {{convert('DECIMAL(2, 0)', 'inputdos')}} as dbxoutputdos,
    '-5.6' as inputtres,
    '-5' as snowoutputtres,
    {{convert('INT', 'inputtres')}} as dbxoutputtres


)

select *
from test
where (snowoutputuno <> dbxoutputuno
	or snowoutputdos <> dbxoutputdos 
	or snowoutputtres <> dbxoutputtres)