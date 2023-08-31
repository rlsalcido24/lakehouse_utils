-- tests/test_dexp.sql

SELECT 
    value,
    {{ dexp('value') }} as exponential_value
FROM
    dbt.dbt_schema.test
