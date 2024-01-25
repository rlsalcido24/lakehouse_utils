
{{
    config(
        materialized = 'table'
    )
}}

select 
    {{lakehouse_utils.convert('string','c_custkey')}} as stringkey,
    c_name,
    c_address,
    c_nationkey,
    c_phone, 
    {{lakehouse_utils.dlog10('c_acctbal')}} as actbalbaseten,
    {{lakehouse_utils.dlog10('c_acctbal')}} as actbalbaseten,
    JSON_EXTRACT_PATH_TEXT('{"f2":{"f3":1},"f4":{"f5":99,"f6":"star"}}','f4', 'f6'),
    {{lakehouse_utils.dexp('100')}},
    {{lakehouse_utils.date_part('dow',' 2008-01-05 14:00:00')}},
    {{lakehouse_utils.hll_cardinality('expr')}},
    JSON_ARRAY_LENGTH('[11,12,13,{"f1":21,"f2":[25,26]},14]'),
    c_mktsegment,
    c_comment,
    {{lakehouse_utils.getdate('')}} as hoy,
    GETDATE AS get_date_caps_test,
    {{lakehouse_utils.sysdate('')}} AS sys_date_col_test,
    {{lakehouse_utils.SYSDATE('')}} AS sys_date_caps_col_test,
    {{lakehouse_utils.ISNULL('test',' test_is_null')}} AS null_test_col_caps,
    {{lakehouse_utils.ISNULL('test',' test_is_null')}} AS null_test_col_caps,
    {{lakehouse_utils.isnull("test"," 'test_is_null'")}} AS null_test_col,
    {{lakehouse_utils.date_part('year',' date(origination_date)')}} || '-' || 'Q' || floor(
            ({{lakehouse_utils.date_part('month',' date(origination_date)')}} - 1) / 3) + 1 as origination_quarter,
    {{lakehouse_utils.date_part("SECONDS"," '2019-10-01 00:00:01.000001'::timestamp")}}
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
