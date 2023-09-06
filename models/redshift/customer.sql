
{{
    config(
        materialized = 'table'
    )
}}


select 
    convet(string, c_custkey) as stringkey,
    c_name,
    c_address,
    c_nationkey,
    c_phone, 
    dlog10(c_acctbal) as actbalbaseten,
    c_mktsegment,
    c_comment,
    getdate() as hoy




from
    redshift_sample_data.tpch_rs1.customer

