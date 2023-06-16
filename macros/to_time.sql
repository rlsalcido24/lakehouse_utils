{% macro to_time(expr) %}
  to_timestamp(expr, 'HH:mm:ss')
{% endmacro %}
