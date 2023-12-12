{% macro isnull(value, if_null_value) %}
   coalesce(value,  if_null_value)
{% endmacro %}
