{% macro dbt_housekeeping() -%}
    '{{ invocation_id }}'::string as dbt_batch_id,
    '{{ run_started_at }}'::timestamp as dbt_batch_ts
{%- endmacro %}
