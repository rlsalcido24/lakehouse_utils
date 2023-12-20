
{{
    config(
        materialized = 'table'
    )
}}

select 
    {{lakehouse_utils.convert("string","c_custkey")}}  as stringkey,
    c_name,
    c_address,
    c_nationkey,
    c_phone, 
    {{lakehouse_utils.dlog10("c_acctbal")}}  as actbalbaseten,
    {{lakehouse_utils.dlog10("c_acctbal")}}  as actbalbaseten,
    c_mktsegment,
    c_comment,
    {{lakehouse_utils.redshift_getdate()}}  as hoy,
    {{lakehouse_utils.redshift_getdate()}}  AS get_date_caps_test,
    {{lakehouse_utils.sysdate()}}  AS sys_date_col_test,
    {{lakehouse_utils.sysdate()}}  AS sys_date_caps_col_test,
    coalesce(test, test_is_null) AS null_test_col_caps,
    coalesce(test, test_is_null) AS null_test_col_caps,
    coalesce(test, 'test_is_null') AS null_test_col,
    first_value(
            case
                when colA = 2
                     then id2
            end ) ignore nulls
          over (
            partition by
                customer_id
            order by
                created_at
            rows between unbounded preceding and unbounded following
        ) as test_syntax_change
from
    redshift_sample_data.tpch_rs1.customer
ORDER BY  colC,colB  DESC NULLS FIRST