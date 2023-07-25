
{{
    config(
        materialized = 'table'
    )
}}


select 
    {{ zeroifnull('c_custkey') }} as intkey,
    {{ contains('c_name','"customer"') }} as namecontains,
    c_address,
    c_nationkey,
    c_phone, 
    {{ to_number ('c_acctbal', 10, 5)}} as cleanacctbal,
    c_mktsegment,
    c_comment




from
    samples.tpch.customer
    
