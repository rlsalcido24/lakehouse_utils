{% macro zeroifnull(column_name) %}
    nvl({{column_name}}, 0)
{% endmacro %}