
{{
    config(
        materialized = 'table'
    )
}}


select 
    zeroifnull(c_custkey) as intkey,
    contains(c_name,'customer') as namecontains,
    c_address,
    c_nationkey,
    c_phone, 
    to_number(c_acctbal, 10, 5) as cleanacctbal,
    c_mktsegment,
    c_comment,
    last_query_id() as lastquery,
    current_transaction() as ct,
    convert_timezone(test),
    to_varchar(test),
    parse_json(testuno),
    parse_json(testdos)




from
    snowflake_sample_data.tpch_sf1.customer

