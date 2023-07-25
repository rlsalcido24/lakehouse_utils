{% macro array_size(column_name) %}
    size({{column_name}})
{% endmacro %}
