
{{
    config(
        materialized = 'table'
    )
}}


select 
     l_orderkey,
     l_partkey,
     l_suppkey,
     l_linenumber,
     l_quantity,
     l_extendedprice,
     l_discount,
     l_tax,
     l_returnflag,
     l_linestatus,
    timestampadd('year', 2, l_shipdate) as shipadd,
    timestampadd('year', 2, l_shipdate) as shipadd,

    timestampdiff('day',l_receiptdate, l_shipdate) as receiptdiff,
    dayname(l_commitdate) as daycommit,
    l_shipinstruct,
    l_shipmode,
    l_comment,
    current_version() as cv,
    get_ddl('table', 'snowflake_sample_data.tpch_sf1.lineitem') as ddl
   

from
     snowflake_sample_data.tpch_sf1.lineitem

