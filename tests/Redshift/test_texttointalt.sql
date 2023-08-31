-- tests/test_texttointalt.sql

SELECT 
    input_expression,
    format_phrase,
    {{ texttointalt('input_expression', 'format_phrase') }} AS result
FROM
    dbt.dbt_schema.test3
