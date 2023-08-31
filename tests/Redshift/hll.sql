with parse as (
SELECT inputuno FROM VALUES (1), (2), (3), (4) AS (inputuno)
),


test as (
    
    select


    4 as redshiftoutput,

    {{hll('inputuno')}} as dbxoutput
    from parse

     
)

select *
from test
where redshiftoutput <> dbxoutput