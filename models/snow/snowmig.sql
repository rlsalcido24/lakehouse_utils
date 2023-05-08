
{{
    config(
        materialized = 'table'
    )
}}

with customers as (

    select * from {{ ref('base_customer') }}

)
select 
    c.customer_key,
    c.customer_name,
    {{ to_varchar('c.customer_address') }} as address,
    {{ zeroifnull('c.nation_key') }} as nationkey,
    {{ contains(1,'c.customer_market_segment_name') }} as marketsegmentbool


from
    customers c
order by
    c.customer_key