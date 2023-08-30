{% macro from_utc_timestamp(source, target, stamp) %}
    from_utc_timestamp(to_utc_timestamp({{stamp}}, {{source}}), {{target}})
{% endmacro %}