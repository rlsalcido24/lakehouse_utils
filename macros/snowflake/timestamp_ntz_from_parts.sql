{% macro timestamp_ntz_from_parts(year, month, day, hour, minute, second) %}
    cast(make_timestamp({{year}}, {{month}}, {{day}}, {{hour}}, {{minute}}, {{second}}) as timestamp_ntz)
{% endmacro %}