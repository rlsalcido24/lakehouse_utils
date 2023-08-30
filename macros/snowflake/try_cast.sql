{% macro try_cast(column_name, precision=2) %}
    cast({{column_name}} as string)
{% endmacro %}
