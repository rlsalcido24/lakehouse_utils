with test as (
    
    select
    '12.3456' as inputuno,
    '12' as snowoutputuno,
    {{to_numeric('inputuno')}} as dbxoutputuno,
    '12.3' as snowoutputunoa,
    '12.3456' as snowoutputunob,
    {{to_numeric('inputuno', 10, 1)}} as dbxoutputunoa ,
    {{to_numeric('inputuno', 10, 8)}} as dbxoutputunob ,
    '98.76546' as inputdos,
    '99' as snowoutputdos,
    '98.8' as snowoutputdosa,
    '98.76546' as snowoutputdosb,
    {{to_numeric('inputdos')}} as dbxoutputdos,
    {{to_numeric('inputdos', 10, 1)}} as dbxoutputdosa,
    {{to_numeric('inputdos', 10, 8)}} as dbxoutputdosb,
    '12.3' as inputtres,
    '12.3' as snowoutputtres,
    '12.3' as snowoutputtresa,
    '12.3' as snowoutputtresb,
    {{to_numeric('inputtres', '99.9')}} as dbxoutputtres,
    {{to_numeric('inputtres', '99.9', 9, 5)}} as dbxoutputtresa,
    {{to_numeric('inputtres', 'TM9', 9, 5)}} as dbxoutputtresb



)

select *
from test
where (snowoutputuno <> dbxoutputuno or snowoutputunoa <> dbxoutputunoa or snowoutputunob <> dbxoutputunob
	or snowoutputdos <> dbxoutputdos or snowoutputdosa <> dbxoutputdosa or snowoutputdosb <> dbxoutputdosb
	or snowoutputtres <> dbxoutputtres or snowoutputtresa <> dbxoutputtresa or snowoutputtresb <> dbxoutputtresb)