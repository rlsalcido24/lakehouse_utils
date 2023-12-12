{{
    config(
        materialized = ‘table’
    )
}}
select
    getdate() AS sys_date_col_test,
    GETDATE() AS sys_date_caps_col_test
from
    redshift_sample_data.tpch_rs1.customer
