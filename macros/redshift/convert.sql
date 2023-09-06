{% macro convert(type, expr) %}
   cast({{expr}} AS {{type}})
{% endmacro %}
