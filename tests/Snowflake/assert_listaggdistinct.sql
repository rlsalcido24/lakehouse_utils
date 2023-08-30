with parse as (

SELECT inputdos FROM VALUES ('F'), ('O'), ('F'), ('O') AS (inputdos)

),


 test as (
    
    select


    "F|O" as snowoutputdos,
    
    {{listagg('distinct inputdos','|')}} as dbxoutputdos
    from parse
group by 1
     
)

select *
from test
where snowoutputdos <> dbxoutputdos
