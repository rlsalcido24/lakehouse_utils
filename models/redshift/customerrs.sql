
{{
    config(
        materialized = 'table'
    )
}}


select 
    {{lakehouse_utils.convert("string"," c_custkey")}} as stringkey,
    c_name,
    c_address,
    c_nationkey,
    c_phone, 
    {{lakehouse_utils.dlog10("c_acctbal")}} as actbalbaseten,
    c_mktsegment,
    c_comment,
    {{lakehouse_utils.getdate()}} as hoy,
    GETDATE AS get_date_caps_test,
    sysdate() AS sys_date_col_test,
    SYSDATE() AS sys_date_caps_col_test,
    ISNULL('test', 'test_is_null') AS null_test_col_caps,
    isnulll('test', 'test_is_null') AS null_test_col,





from
    redshift_sample_data.tpch_rs1.customer

