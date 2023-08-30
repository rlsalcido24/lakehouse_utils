with parse as (
SELECT inputuno FROM VALUES (41445), (55937), (67781), (80550) AS (inputuno)
),


test as (
    
    select


    "41445 55937 67781 80550" as snowoutputuno,

    {{listagg('inputuno',' ')}} as dbxoutputuno
    from parse
group by 1
     
)

select *
from test
where snowoutputuno <> dbxoutputuno
