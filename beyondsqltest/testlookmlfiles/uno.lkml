uno = """{{
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
    dlog10(c_acctbal) as actbalbaseten,
    dlog10(c_acctbal) as actbalbaseten,
    JSON_EXTRACT_PATH_TEXT('{"f2":{"f3":1},"f4":{"f5":99,"f6":"star"}}','f4', 'f6'),
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
    ISNULL(test, test_is_null) AS null_test_col_caps,
    ISNULL(test, test_is_null) AS null_test_col_caps,
    isnull(test, 'test_is_null') AS null_test_col,
    date_part(year, date(origination_date)) || '-' || 'Q' || floor(
            (date_part(month, date(origination_date)) - 1) / 3) + 1 as origination_quarter,
    date_part(SECONDS, '2019-10-01 00:00:01.000001'::timestamp)
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
ORDER BY colC,colB DESC)"""
print(uno)