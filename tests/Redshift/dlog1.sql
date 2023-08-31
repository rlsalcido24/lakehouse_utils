with

 test as (
    
    select


    1 as redshiftoutput,
    
    {{dlog1(2.718281828)}} as dbxouput
     
)

select *
from test
where redshiftoutput <> dbxoutput