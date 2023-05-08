
{{
    config(
        materialized = 'table'
    )
}}


select 
    c.customer_key,
    c.customer_name,
    {{ to_varchar('c.customer_address') }} as address,
    {{ zeroifnull('c.nation_key') }} as nationkey,
    {{ contains(1,'c.customer_market_segment_name') }} as marketsegmentbool


from
    robertotpch.customers c
order by
    c.customer_key
