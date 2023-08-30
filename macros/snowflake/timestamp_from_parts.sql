{% macro timestamp_from_parts(year, month, day, hour, minute, second) %}
   make_timestamp({{year}}, {{month}}, {{day}}, {{hour}}, {{minute}}, {{second}})
{% endmacro %}
