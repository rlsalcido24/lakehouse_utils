
{{
    config(
        materialized = 'table'
    )
}}

select 
    convert(string,c_custkey) as stringkey,
    c_name,
    c_address,
    c_nationkey,
    c_phone, 
    (to_char(date_trunc('month', getdate()), 'YYYY-MM')) as month,
    datediff(days, getdate(), getdate()) as days_since_oldest_unpaid_due_date,
    datediff(hours, getdate(), getdate()) as days_since_oldest_unpaid_due_date
    date_trunc('months', getdate()),
    date_trunc('hours', getdate()),
    dateadd(day, -1, getdate()),
    case when 'organictest' ~ 'organic|email' then 'match' else 'no match' end as regexmatch,
    case when 'organictest' !~ 'organic|email' then 'antimatch' else 'antino match' end as antiregexmatch
    dlog10(c_acctbal) as actbalbaseten,
    dlog10(c_acctbal) as actbalbaseten,
    JSON_EXTRACT_PATH_TEXT('{"f2":{"f3":1},"f4":{"f5":99,"f6":"star"}}','f4', 'f6'),
    JSON_EXTRACT_PATH_TEXT(NULLIF(REPLACE(REPLACE( REPLACE(related_videos, '\\', ''), '"{', ''), '}"', ''), ''), 'id')
    dexp(100),
    date_part(dow, 2008-01-05 14:00:00),
    hll_cardinality(expr),
    JSON_ARRAY_LENGTH('[11,12,13,{"f1":21,"f2":[25,26]},14]'),
    c_mktsegment,
    c_comment,
    getdate() as hoy,
    GETDATE AS get_date_caps_test,
    sysdate() AS sys_date_col_test,
    SYSDATE() AS sys_date_caps_col_test,
    Name,
    Age,
    CAST(ID AS TEXT) as id_text,
    created_date::TIME,
    CAST(file_dump AS NUMERIC) as file_dump_numeric,
    COALESCE(col1::FLOAT,col2::FLOAT8,col3::INT2) AS xyz
    FROM catalog.schema.table1
    WHERE colA = colB::CHAR
    AND somethingelse = 1
    ISNULL(test, test_is_null) AS null_test_col_caps,
    ISNULL(test, test_is_null) AS null_test_col_caps,
    isnull(test, 'test_is_null') AS null_test_col,
    date_part(year, date(origination_date)) || '-' || 'Q' || floor(
            (date_part(month, date(origination_date)) - 1) / 3) + 1 as origination_quarter,
    date_part(SECONDS, '2019-10-01 00:00:01.000001'::timestamp),
    first_value(
            case when colA = 2 then id2
            end ignore nulls
        ) over (
            partition by
                customer_id
            order by
                created_at
            rows between unbounded preceding and unbounded following
        ) as test_syntax_change
from
    redshift_sample_data.tpch_rs1.customer
ORDER BY colC,colB DESC