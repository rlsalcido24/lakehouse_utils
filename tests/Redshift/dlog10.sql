with

 test as (
    
    select


    2 as redshiftoutput,
    
    {{dlog10(100)}} as dbxouput
     
)

select *
from test
where redshiftoutput <> dbxoutput