{{
    config(
        materialized = ‘table’
    )
}}
select
    sysdate() AS sys_date_col_test,
    SYSDATE() AS sys_date_caps_col_test
from
    redshift_sample_data.tpch_rs1.customer
