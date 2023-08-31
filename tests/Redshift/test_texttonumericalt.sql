-- tests/test_texttonumericalt.sql

WITH test AS (SELECT 
    123.5201 as testnum,
    10 as precision,
    2 as scale
)

SELECT ROUND(CAST(testnum AS DECIMAL(PRECISION, scale)), scale) FROM test;
